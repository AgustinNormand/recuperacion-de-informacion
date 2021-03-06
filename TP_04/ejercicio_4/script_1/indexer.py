import pathlib
from exporter import Exporter
from tokenizer import Tokenizer
from multiprocessing import Queue
import time
import threading
from constants import *

def process_function(exporter, worker_number, queue):
    while True:
        process_block = queue.get()
        if process_block == "":
            break
        process_block_number, process_block = process_block
        tokenizer = Tokenizer()
        for value in process_block:
            try:
                tokenizer.tokenize_file(value[0], value[1])
            except Exception as e:
                print(e)
        results = tokenizer.get_results()
        exporter.save_process_block(results, worker_number, process_block_number)


class Indexer:
    def __init__(self):
        self.exporter = Exporter()
        self.load_documents()
        self.build_workers_queue()
        self.index()
        self.exporter.compute_vocabulary()

        print("Indexing time: {} seconds.".format(self.index_time))
        start = time.time()
        self.exporter.merge_inverted_index()
        end = time.time()

        print("Mergeing time: {} seconds.".format(end - start))
        self.exporter.vocabulary_file()
        self.exporter.metadata()

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

        self.docnames_ids = dict(
            sorted(self.docnames_ids.items(), key=lambda item: item[1])
        )
        self.exporter.save_docnames_ids_file(self.docnames_ids)
        self.document_limit = DOCUMENT_LIMIT
        print("Limite de documentos: {}".format(self.document_limit))

    def build_workers_queue(self):
        self.queue = Queue()

        document_counter = 0
        process_block = []
        process_block_counter = 0
        for docname_id in self.docnames_ids:
            process_block.append([docname_id, self.docnames_ids[docname_id]])
            document_counter += 1
            if document_counter == self.document_limit:
                self.queue.put([process_block_counter, process_block])
                process_block_counter += 1
                document_counter = 0
                process_block = []

        if document_counter > 0:
            self.queue.put([process_block_counter, process_block])

        for i in range(WORKERS_NUMBER):
            self.queue.put("")

    def index(self):
        start = time.time()

        threads = []
        for worker_number in range(WORKERS_NUMBER):
            p = threading.Thread(
                target=process_function,
                args=(self.exporter, worker_number, self.queue),
            )
            threads.append(p)
            p.start()

        for thread in threads:
            thread.join()

        end = time.time()

        self.index_time = end - start