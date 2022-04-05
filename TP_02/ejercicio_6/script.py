import sys
import pathlib
from tokenizer import Tokenizer
from exporter import Exporter
import queue, time, urllib.request
from threading import Thread

class Model:
	def __init__(self, dirpath):
		self.corpus_path = pathlib.Path(dirpath)
		self.docnames_ids = {}
		self.document_vectors = {}
		self.vocabulary = {}

		self.tokenizer = Tokenizer()

		#self.process_dir()

		self.distribute_load(self.corpus_path.rglob("*.*"), 10)

		Exporter(self.docnames_ids, self.document_vectors, self.vocabulary)

	def process_dir(self):

		id_count = 1
		for file_name in self.corpus_path.rglob("*.*"):
			doc_id = id_count
			id_count += 1
			self.docnames_ids[str(file_name)] = doc_id
			self.document_vectors[doc_id] = self.tokenizer.tokenize_file(file_name)

		self.vocabulary = self.tokenizer.get_vocabulary()
	


	def distribute_load(self, corpus_path, no_workers):
		class Worker(Thread):
			def __init__(self, filenames_queue):
				Thread.__init__(self)
				self.queue = filenames_queue
				self.tokenizer = Tokenizer()

			def run(self):
				while True:
					content = self.queue.get()
					if content == "":
						break
					try:
						self.tokenizer.tokenize_file(content)
					except Exception as e:
						pass
					self.queue.task_done()

		q = queue.Queue()
		for filename in corpus_path:
			q.put(filename)

		workers = []
		for _ in range(no_workers):
			worker = Worker(q)
			worker.start()
			workers.append(worker)

		for _ in workers:
			q.put("")

		for worker in workers:
			worker.join()

		e = []
		for worker in workers:
			e.extend(worker.errors)

		return e

#errors, record_count = perform_web_requests(resources_with_neighborhood, 25)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Es necesario pasar como argumento un path a un directorio')
		sys.exit(0)
	dirpath = sys.argv[1]

	import time
	start = time.time()
	Model(dirpath)
	end = time.time()
	print("\r\nExecution time: {} seconds.".format(end - start))

