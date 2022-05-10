import pathlib
from exporter import Exporter
from tokenizer import Tokenizer
from multiprocessing import Manager, Queue
import time
import threading
from constants import *
import merger as merger

def process_function(worker_number, queue, results):
    tokenizer = Tokenizer()
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
                content[0], content[1]
            )

        except Exception as e:
            print(e)

    results.append(tokenizer.get_results())


class Indexer:
    def __init__(self):
        self.exporter = Exporter()
        self.load_documents()
        self.index()

    def load_documents(self):
        corpus_path = pathlib.Path(DIRPATH)
        self.docnames_ids = {}
        id_count = 1
        for file_name in corpus_path.rglob("*.*"): ##If docnames are docNNNN.txt
            if ID_IN_DOCNAME:
                doc_id = int(file_name.stem.split("doc")[1])
            else:
                doc_id = id_count
                id_count += 1
            self.docnames_ids[str(file_name.resolve())] = doc_id
        
        self.exporter.save_docnames_ids_file(self.docnames_ids)
        

    def index(self):
        with Manager() as manager:
            queue = Queue()
            results = manager.list()
            for docname_id in self.docnames_ids:
                queue.put([docname_id, self.docnames_ids[docname_id]])

            workers_number = WORKERS_NUMBER
            for i in range(workers_number):
                queue.put("")

            start = time.time()

            threads = []
            for worker_number in range(workers_number):
                p = threading.Thread(
                    target=process_function,
                    args=(worker_number, queue, results),
                )
                threads.append(p)
                p.start()

            for thread in threads:
                thread.join()

            end = time.time()
            print("\r                                   ")
            print(
                "\rDistributed Indexing time: {} seconds, Documents Processed: {}, Workers Threads: {}.".format(
                    end - start, len(self.docnames_ids), workers_number
                )
            )

            start = time.time()
            (
                vocabulary,
                inverted_index,
                index
            ) = merger.process_results(results)
            end = time.time()
            print("\rMergeing time: {} seconds.".format(end - start))
            
            self.exporter.vocabulary_file(vocabulary)
            self.exporter.inverted_index(inverted_index)
            self.exporter.ids_norm(index)
            self.exporter.metadata()

            #self.exporter.export_all_statistics()

            print("Files exported.")

             


