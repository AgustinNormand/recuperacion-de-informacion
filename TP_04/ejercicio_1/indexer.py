import pathlib
import sys
from exporter import Exporter
from tokenizer import Tokenizer
from multiprocessing import Manager, Queue
import time
import threading
import merger


def process_function(worker_number, queue, stopwords_path, results):
    tokenizer = Tokenizer(stopwords_path)
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
    def __init__(self, dirpath, stopwords_path):
        self.dirpath = dirpath
        self.load_documents(dirpath)
        self.index(stopwords_path)

    def load_documents(self, dirpath):
        corpus_path = pathlib.Path(dirpath)
        self.docnames_ids = {}
        id_count = 1
        for file_name in corpus_path.rglob("*.*"):
            doc_id = id_count
            id_count += 1
            self.docnames_ids[str(file_name.resolve())] = doc_id
        Exporter().set_docnames_ids_file(self.docnames_ids, "./output/docnames_ids.bin")


    def index(self, stopwords_path):
        with Manager() as manager:
            queue = Queue()
            results = manager.list()
            for docname_id in self.docnames_ids:
                # Queue = ([docpath, docid], [...])
                queue.put([docname_id, self.docnames_ids[docname_id]])

            workers_number = 5
            for i in range(workers_number):
                queue.put("")

            start = time.time()

            threads = []
            for worker_number in range(workers_number):
                p = threading.Thread(
                    target=process_function,
                    args=(worker_number, queue, stopwords_path, results),
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
                documents_vectors,
            ) = merger.process_results(results)
            end = time.time()
            print("\rMergeing time: {} seconds.".format(end - start))
            #print(vocabulary)
            print(vocabulary)
            #Exporter().vocabulary_file(vocabulary, "./output/vocabulary")
            #Exporter().inverted_index(inverted_index, "./output/inverted_index")
            #Exporter().documents_vectors(documents_vectors, "./output/documents_vectors")
            #Exporter().documents_norm(documents_norm, "./output/documents_norm")

            #print("Human readable and .pkl files exported.")
            """
            return [
                docnames_ids,
                vocabulary,
                inverted_index,
                documents_vectors,
                documents_norm,
            ]
            """


#dirpath = None

#if len(sys.argv) > 1:
    #dirpath = sys.argv[1]
    #i = Indexer(dirpath)
