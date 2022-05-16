import pathlib
from exporter import Exporter
from tokenizer import Tokenizer
from multiprocessing import Manager, Queue
import time
import threading
import merger
from constants import *


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
        self.exporter.analize_document_titles_length(self.docnames_ids)
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
            ) = merger.process_results(results)
            end = time.time()
            print("\rMergeing time: {} seconds.".format(end - start))
            
            print("Vocabulary")
            print(vocabulary)

            self.exporter.inverted_index(inverted_index)
            self.exporter.vocabulary_file(vocabulary)

            #self.exporter.postings_distribution(inverted_index)
            #if COMPUTE_OVERHEAD:
                #self.exporter.collection_overhead()
                #self.exporter.document_overhead(self.docnames_ids, inverted_index)
            self.exporter.metadata()

            print("Files exported.")

"""
Almacené los punteros calculados, es decir, solo es necesario hacer un seek al puntero. Esto no es lo mejor, ya que se requieren más bits para almacenar el puntero, lo cual trae diversas desventajas, en la compresión, en la lectura de mayor cantidad de registros por ciclos de cpu, overhead, etc. Y la única ventaja es ahorrarse un cálculo en query time, que es, el puntero multiplicado por el tamaño en bytes del string_format usado en el struct.
Si la posting es [1, 2, 3, 4, 5, 6], en las skips con un K de 3, guardo 3:3, 6:6 y leo 3

"""


