from multiprocessing import Manager, Queue
import pathlib
from tokenizer import Tokenizer
from exporter import Exporter
import threading
import time
import merger


def load_documents(corpus_path):
    docnames_ids = {}
    id_count = 1
    for file_name in corpus_path.rglob("*.*"):
        doc_id = id_count
        id_count += 1
        docnames_ids[str(file_name)] = doc_id
    Exporter().docnames_ids_file(docnames_ids, "./output/docnames_ids")
    return docnames_ids


def process_function(worker_number, queue, stopwords_path, results):
    tokenizer = Tokenizer(stopwords_path)
    if worker_number == 1:
        total = queue.qsize()

    while True:
        if worker_number == 1:
            print("\r                                   ", end="")
            print("\r{}%".format(1-(queue.qsize()/total)), end="")
        content = queue.get()
        if content == "":
            break
        try:
            tokenizer.tokenize_file(content[0], content[1], pathlib.Path(content[0]).suffix == ".html")
                
            
        except Exception as e:
            print(e)

    results.append(tokenizer.get_results())


def index(dirpath, stopwords_path):
    corpus_path = pathlib.Path(dirpath)

    docnames_ids = load_documents(corpus_path)

    with Manager() as manager:
        queue = Queue()
        results = manager.list()

        for docname_id in docnames_ids:
            # Queue = ([docpath, docid], [...])
            queue.put([docname_id, docnames_ids[docname_id]])

        workers_number = 5
        for i in range(workers_number):
            queue.put("")

        start = time.time()

        threads = []
        for worker_number in range(workers_number):
            p = threading.Thread(target=process_function, args=(
                worker_number, queue, stopwords_path, results))
            threads.append(p)
            p.start()

        for thread in threads:
            thread.join()

        end = time.time()
        print("\rDistributed Indexing time: {} seconds, Documents Processed: {}, Workers Threads: {}.".format(
            end - start, len(docnames_ids), workers_number))

        start = time.time()
        vocabulary, inverted_index, documents_vectors, documents_norm = merger.process_results(
            results)
        end = time.time()
        print("\rMergeing time: {} seconds.".format(end - start))

        Exporter().vocabulary_file(vocabulary, "./output/vocabulary")
        Exporter().inverted_index(inverted_index, "./output/inverted_index")
        Exporter().documents_vectors(documents_vectors, "./output/documents_vectors")
        Exporter().documents_norm(documents_norm, "./output/documents_norm")

        print("Human readable and .pkl files exported.")

        return [docnames_ids, vocabulary, inverted_index, documents_vectors, documents_norm]
