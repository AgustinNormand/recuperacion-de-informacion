from multiprocessing import Manager, Queue
import sys
import pathlib
from tokenizer import Tokenizer
from exporter import Exporter
import threading
import pickle
import time
from model import Model

def show_menu(model):
	tokenizer = Tokenizer()
	print("Ingrese los terminos de la query, 0 para salir.")
	user_input = ""
	while user_input != "0":
		user_input = input()
		if user_input != "0":
			model.query(tokenizer.tokenize_query(user_input))

def load_documents(corpus_path):
	docnames_ids = {}
	id_count = 1
	for file_name in corpus_path.rglob("*.*"):
		doc_id = id_count
		id_count += 1
		docnames_ids[str(file_name)] = doc_id
	return docnames_ids

def translate_document_vector(vocabulary, document_vector):
	result = {}
	for value in document_vector:
		result[vocabulary[value][0]] = document_vector[value]
	return result

def get_df(value, results):
	acum = 0
	for result in results: #results = [[vocab, docvec], [vocab, docvec]] 1 por cada thread
		try:
			vocabulary = result[0]
			acum += vocabulary[value]
		except:
			pass
	return acum

def process_results(results):
	keys = []
	for result in results: #results = [[vocab, docvec], [vocab, docvec]] 1 por cada thread
		vocabulary = result[0]

		keys.extend(vocabulary.keys())
	vocabulary_list = list(set(keys))

	vocabulary = {}
	id_counter = 1

	for value in vocabulary_list:
		vocabulary[value] = [id_counter, get_df(value, results)]
		id_counter += 1

	cleaned_documents_vectors = {}

	for result in results:
		documents_vectors = result[1]
		for key in documents_vectors:
			cleaned_documents_vectors[key] = documents_vectors[key]
			#cleaned_documents_vectors[key] = translate_document_vector(vocabulary, documents_vectors[key])

	return [vocabulary, cleaned_documents_vectors]

def use_saved_index(dirpath):
	corpus_path = pathlib.Path(dirpath)
	docnames_ids = load_documents(corpus_path)
	file = open('result_list', 'rb')
	results = []
	while True:
		try:
			results.append(pickle.load(file))
		except:
			break
	file.close()
	
	vocabulary, documents_vectors = process_results(results)

	#Exporter(docnames_ids, documents_vectors, vocabulary)
	
	show_menu(Model(vocabulary, documents_vectors, docnames_ids))
	sys.exit()


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
			tokenizer.tokenize_html_file(content[0], content[1])
		except Exception as e:
			print(e)
		
	results.append(tokenizer.get_results())

def index(dirpath):
	corpus_path = pathlib.Path(dirpath)

	docnames_ids = load_documents(corpus_path)

	with Manager() as manager:
		queue = Queue()
		results = manager.list()

		for docname_id in docnames_ids:
			queue.put([docname_id, docnames_ids[docname_id]])   #Queue = ([docpath, docid], [...])

		workers_number = 5
		for i in range(workers_number):
			queue.put("")
	
		
		start = time.time()

		threads = []
		for worker_number in range(workers_number):
			p = threading.Thread(target=process_function, args=(worker_number, queue, results))
			threads.append(p)
			p.start()

		for thread in threads:
			thread.join()

		end = time.time()
		print("\rDistributed Indexing time: {} seconds.".format(end - start))

		file = open('result_list', 'wb')
		for result in results:
			pickle.dump(result, file)
		file.close()

		#start = time.time()
		#vocabulary, documents_vectors = process_results(results)
		#end = time.time()
		#print("\rMergeing thread results time: {} seconds.".format(end - start))

		#Exporter(docnames_ids, documents_vectors, vocabulary)

if __name__ == '__main__':
	
	if len(sys.argv) < 3:
		print('Es necesario pasar como argumento un path a un directorio')
		print('Como también 1 si quiere indexar o 0 si quiere usar el indice de disco')
		sys.exit(0)

	dirpath = sys.argv[1]

	indexar = int(sys.argv[2])

	if indexar == 0:
		use_saved_index(dirpath)
	else:
		index(dirpath)
	

		#


#799.2709686756134 seconds.
#\rIndexing time: 133.31357550621033 seconds.
	