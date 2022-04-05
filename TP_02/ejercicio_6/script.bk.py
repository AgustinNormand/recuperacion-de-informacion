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

		self.process_dir()

		Exporter(self.docnames_ids, self.document_vectors, self.vocabulary)

	def process_dir(self):

		id_count = 1
		for file_name in self.corpus_path.rglob("*.*"):
			doc_id = id_count
			id_count += 1
			self.docnames_ids[str(file_name)] = doc_id
			self.document_vectors[doc_id] = self.tokenizer.tokenize_file(file_name)

		self.vocabulary = self.tokenizer.get_vocabulary()

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

