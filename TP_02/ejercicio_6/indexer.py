from multiprocessing import Manager, Queue
import sys
import pathlib
from tokenizer import Tokenizer
from exporter import Exporter
import threading
import pickle

from model import Model

def load_documents(corpus_path):
	docnames_ids = {}
	id_count = 1
	for file_name in corpus_path.rglob("*.*"):
		doc_id = id_count
		id_count += 1
		docnames_ids[str(file_name)] = doc_id
	return docnames_ids
	
def process_function(worker_number, queue, results):
	tokenizer = Tokenizer()
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
			tokenizer.tokenize_file(content[0], content[1])
		except Exception as e:
			print(e)
		
	results.append(tokenizer.get_results())


def translate_document_vector(vocabulary, document_vector):
	result = {}
	for value in document_vector:
		result[vocabulary[value]] = document_vector[value]
	return result

def process_results(results):
	keys = []
	for result in results: #results = [[vocab, docvec], [vocab, docvec]] 1 por cada thread
		vocabulary = result[0]

		#sys.exit()
		keys.extend(vocabulary.keys())
	vocabulary_list = list(set(keys))

	vocabulary = {}
	id_counter = 1

	for value in vocabulary_list:
		vocabulary[value] = id_counter
		id_counter += 1

	cleaned_documents_vectors = {}

	for result in results:
		documents_vectors = result[1]
		for key in documents_vectors:
			cleaned_documents_vectors[key] = translate_document_vector(vocabulary, documents_vectors[key])

	return [vocabulary, cleaned_documents_vectors]
	#print(len(cleaned_documents_vectors.keys()))
	#print(vocabulary)

def simulate(docnames_ids):
	file = open('result_list', 'rb')
	results = []
	while True:
		try:
			results.append(pickle.load(file))
		except:
			break
	file.close()
	
	vocabulary, documents_vectors = process_results(results)

	Exporter(docnames_ids, documents_vectors, vocabulary)
	m = Model(vocabulary, documents_vectors, docnames_ids)
	sys.exit()

if __name__ == '__main__':
	
	if len(sys.argv) < 2:
		print('Es necesario pasar como argumento un path a un directorio')
		sys.exit(0)
	dirpath = sys.argv[1]
	
	corpus_path = pathlib.Path(dirpath)

	docnames_ids = load_documents(corpus_path)


	#simulate(docnames_ids)



	with Manager() as manager:
		queue = Queue()
		results = manager.list()

		for docname_id in docnames_ids:
			queue.put([docname_id, docnames_ids[docname_id]])   #Queue = ([docpath, docid], [...])

		workers_number = 3
		for i in range(workers_number):
			queue.put("")
	
		import time
		start = time.time()

		threads = []
		for worker_number in range(workers_number):
			p = threading.Thread(target=process_function, args=(worker_number, queue, results))
			threads.append(p)
			p.start()

		for thread in threads:
			thread.join()

		end = time.time()
		print("\rIndexing time: {} seconds.".format(end - start))

		start = time.time()
		vocabulary, documents_vectors = process_results(results)
		end = time.time()
		print("\rMergeing thread results time: {} seconds.".format(end - start))

		#Exporter(docnames_ids, documents_vectors, vocabulary)
		#m = Model(vocabulary, documents_vectors, docnames_ids)

		file = open('result_list', 'wb')
		for result in results:
			pickle.dump(result, file)
		file.close()

		#


#799.2709686756134 seconds.
#\rIndexing time: 133.31357550621033 seconds.
	