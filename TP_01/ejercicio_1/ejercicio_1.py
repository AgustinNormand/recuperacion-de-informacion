import sys
import matplotlib.pyplot as plt

from normalizer import Normalizer
from collection import Collection
from document import Document

class Text_analyzer:

	def __init__(self, dirpath, empty_words_path):
		self.palabras_vacias = []
		self.min_length = 0
		self.max_length = 10

		self.term_frequencies = {}

		#self.load_empty_words()

		self.collection = Collection(dirpath)

		self.process_collection()

		print(self.term_frequencies)

	#def load_empty_words(self):
		#if delete_empty_words == "True":
		#	with open(empty_words_path, "r") as f:
		#		for line in f.readlines():
		#			self.palabras_vacias.extend(line.split(","))

	def valid_length(self, token): 
		return (len(token) > self.min_length and len(token) < self.max_length)

	def is_term(self, token):
		if token not in self.palabras_vacias:
			if self.valid_length(token):
				return True
			else:
				return False
		else:
			return False

	def process_collection(self):
		n = Normalizer()
		documents = self.collection.get_documents()

		for document in documents:
			document_word_list = document.get_words_list()

			document_tokens = []
			unique_document_terms = []

			for document_word in document_word_list:
				document_token = n.normalize(document_word)
					
				document_tokens.append(document_token)

				is_valid_term = self.is_term(document_token)

				self.increment_term_collection_frequency(document_token)

				if is_valid_term and document_token not in unique_document_terms:
					unique_document_terms.append(document_token)

			self.increment_document_frequency(unique_document_terms)

			document.set_tokens(document_tokens)
			document.set_terms(unique_document_terms)

			

	def increment_term_collection_frequency(self, term):
		if term in self.term_frequencies.keys():
			self.term_frequencies[term][0] += 1
		else:
			self.term_frequencies[term] = [1, 0]  


	def increment_document_frequency(self, document_terms):
		for term in document_terms:
			# Incremento la frecuencia en el documento
			self.term_frequencies[term][1] += 1

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('Es necesario pasar los siguientes argumentos:')
		print('Path al directorio de la coleccion')
		print("Opcional: Path al archivo de palabras vacias.")
		sys.exit(0)

	empty_words_path = None
	#if (sys.argv[2] == 'True'):
		#if len(sys.argv) < 4:
			#print('Indicar el Path al archivo de palabras vacias')
			#sys.exit(0)
		#else:
			#empty_words_path = sys.argv[3]

	dirpath = sys.argv[1]
	#delete_empty_words = sys.argv[2]

	import time

	start = time.time()
	ta = Text_analyzer(dirpath, empty_words_path)
	end = time.time()
	print("\r\nExecution time: {} seconds.".format(end - start))

	#4.8, 5.62 segundos tiempo ejecución
