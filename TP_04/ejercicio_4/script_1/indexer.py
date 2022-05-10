import pathlib
from exporter import Exporter
from tokenizer import Tokenizer
from multiprocessing import Manager, Queue
import time
import threading
import merger
from constants import *


def process_function(worker_number, queue):
    exporter = Exporter()
    process_block_count = 0
    while True:
        process_block = queue.get()
        if process_block == "":
            break
        try:
            process_block_count += 1
            tokenizer = Tokenizer()
            for value in process_block:
                tokenizer.tokenize_file(value[0], value[1])
            exporter.save_process_block(tokenizer.get_results(), worker_number, process_block_count)
        except Exception as e:
            print(e)


class Indexer:
    def __init__(self):
        self.exporter = Exporter()
        self.load_documents()
        self.build_workers_queue()
        self.index()

    def load_documents(self):
        corpus_path = pathlib.Path(DIRPATH)
        self.docnames_ids = {}
        id_count = 1
        for file_name in corpus_path.rglob("*.*"):
            if ID_IN_DOCNAME:
                doc_id = int(file_name.stem.split("doc")[1])
            else:
                doc_id = id_count
                id_count += 1
            self.docnames_ids[str(file_name.resolve())] = doc_id
        self.exporter.save_docnames_ids_file(self.docnames_ids)
        self.document_limit = len(self.docnames_ids) * 0.1
        print("Limite de documentos: {}".format(self.document_limit))

    
    def build_workers_queue(self):
        self.queue = Queue()

        document_counter = 0
        process_block = []
        for docname_id in self.docnames_ids:
            process_block.append([docname_id, self.docnames_ids[docname_id]])
            document_counter += 1
            if document_counter == self.document_limit:
                self.queue.put(process_block)
                document_counter = 0
                process_block = []

        if document_counter > 0:
            self.queue.put(process_block)
        
        for i in range(WORKERS_NUMBER):
            self.queue.put("")

    def index(self):

        start = time.time()

        threads = []
        for worker_number in range(WORKERS_NUMBER):
            p = threading.Thread(
                target=process_function,
                args=(worker_number, self.queue),
            )
            threads.append(p)
            p.start()

        for thread in threads:
            thread.join()

        end = time.time()
        print("\r                                   ")
        print(
            "\rDistributed Indexing time: {} seconds, Documents Processed: {}, Workers Threads: {}.".format(
                end - start, len(self.docnames_ids), WORKERS_NUMBER
            )
        )

        """start = time.time()
            (
                vocabulary,
                inverted_index,
            ) = merger.process_results(results)
            
            end = time.time()
            print("\rMergeing time: {} seconds.".format(end - start))
            
            self.exporter.vocabulary_file(vocabulary)
            self.exporter.inverted_index(inverted_index)
            self.exporter.metadata()

            print("Files exported.")
            """
