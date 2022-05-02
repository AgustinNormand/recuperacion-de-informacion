import pathlib
from exporter import Exporter
from tokenizer import Tokenizer
from multiprocessing import Manager, Queue
import time
import threading
import merger


def process_function(worker_number, queue, stopwords_path, stemming_language, extract_entities, results):
    tokenizer = Tokenizer(stopwords_path, stemming_language, extract_entities)
    if worker_number == 1:
        total = queue.qsize()

    while True:
        if worker_number == 1:
            print("\r                                   ", end="")
            print("\r{}%".format(1 - (queue.qsize() / total)), end="")
        content = queue.get()
        if content == "":
            break
        try:
            tokenizer.tokenize_file(
                content[0], content[1], pathlib.Path(content[0]).suffix == ".html"
            )

        except Exception as e:
            print(e)

    results.append(tokenizer.get_results())


class Indexer:
    def __init__(self, dirpath, stopwords_path, stemming_language, extract_entities):
        
        self.stemming_language = stemming_language
        self.extract_entities = extract_entities
        self.dirpath = dirpath
        self.stopwords_path = stopwords_path
        self.load_documents(dirpath, True)
        self.index()

    def load_documents(self, dirpath, id_in_name = False):
        corpus_path = pathlib.Path(dirpath)
        self.docnames_ids = {}
        id_count = 1
        for file_name in corpus_path.rglob("*.*"): ##If docnames are docNNNN.txt
            if id_in_name:
                doc_id = int(file_name.stem.split("doc")[1])
            else:
                doc_id = id_count
                id_count += 1
            self.docnames_ids[str(file_name.resolve())] = doc_id
        Exporter().set_docnames_ids_file(self.docnames_ids, "./output/docnames_ids")

    def index(self):
        with Manager() as manager:
            queue = Queue()
            results = manager.list()
            for docname_id in self.docnames_ids:
                queue.put([docname_id, self.docnames_ids[docname_id]])

            workers_number = 5
            for i in range(workers_number):
                queue.put("")

            start = time.time()

            threads = []
            for worker_number in range(workers_number):
                p = threading.Thread(
                    target=process_function,
                    args=(worker_number, queue, self.stopwords_path, self.stemming_language, self.extract_entities, results),
                )
                threads.append(p)
                p.start()

            for thread in threads:
                thread.join()

            end = time.time()
            print(
                "\rDistributed Indexing time: {} seconds, Documents Processed: {}, Workers Threads: {}.".format(
                    end - start, len(self.docnames_ids), workers_number
                )
            )

            start = time.time()
            (
                vocabulary,
                inverted_index,
            ) = merger.process_results(results)
            end = time.time()
            print("\rMergeing time: {} seconds.".format(end - start))
            
            Exporter().vocabulary_file(vocabulary, "./output/vocabulary")
            Exporter().inverted_index(inverted_index, "./output/inverted_index")

            print("Files exported.")

