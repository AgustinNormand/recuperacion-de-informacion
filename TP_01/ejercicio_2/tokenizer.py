import sys
import matplotlib.pyplot as plt

from normalizer import Normalizer
from collection import Collection
from document import Document
from exporter import Exporter
import re

class Tokenizer:
	def __init__(self, dirpath, empty_words_path):
		self.palabras_vacias = []
		self.min_length = 3
		self.max_length = 20

		self.term_frequencies = {}
		self.token_list = []

		self.term_length_acumulator = 0

		self.load_empty_words(empty_words_path)

		self.collection = Collection(dirpath)

		self.process_collection()

		#Exporter(self.term_frequencies, self.token_list, self.term_length_acumulator, self.collection).generate_files()

	def load_empty_words(self, empty_words_path):
		if empty_words_path:
			with open(empty_words_path, "r") as f:
				for line in f.readlines():
					self.palabras_vacias.extend(line.split(","))

	def valid_length(self, token): 
		return (len(token) > self.min_length and len(token) < self.max_length)

	def is_term(self, token):
		return token not in self.palabras_vacias and self.valid_length(token)

	def process_collection(self):
		n = Normalizer()
		documents = self.collection.get_documents()

		for document in documents:
			document_word_list = document.get_words_list()

			document_tokens = []
			unique_document_terms = []

			for document_word in document_word_list:

				if self.get_token_type(document_word) == "test":
					print(document_word)

				document_token = n.normalize(document_word)
					
				document_tokens.append(document_token)

				self.token_list.append(document_token)

				is_valid_term = self.is_term(document_token)

				if is_valid_term:
					self.increment_term_collection_frequency(document_token)
					
					if document_token not in unique_document_terms:
						unique_document_terms.append(document_token)
					

			self.increment_document_frequency(unique_document_terms)

			document.set_tokens(document_tokens)
			document.set_terms(unique_document_terms)

	def get_token_type(self, document_word):
		regular_expressions = [
			["([A-Z]{3})", "test"]
			#["([a-zA-Z0-9]+@[a-z.]+)", "email"],
			#["(https?://[a-zA-Z./0-9-_?=]+)", "url"],
			#["([A-Z][a-z]+\.)", "abbreviation"], # Dr. Lic.
			#["([A-Z]\.)", "abbreviation"], #S.A. #Este tiene que ir antes del de "etc."
			#["([a-z]+\.)", "abbreviation"], # etc.
			#["([A-Z]{4})", "abbreviation"], # NASA Esto no matchea solo4  veces, ASESINADO PARTICIPARON DECLARACION
			#["([a-zA-Z]+[0-9]*[^A-Za-z0-9]*)", "general"], # Matcheo todo lo que no sea numeros
			#["([0-9]+)", "number"], # Estoo matchea fisica1 docente1 economicas1 #Este no funcaba bien ( [0-9]+ ) matchea solo si tiene espacios adelante y atrás
			#["([0-9]+\.[0-9]+)", "number"], # Decimales "(\b[0-9]+\.[0-9]+\b)" Tambien matchea 2.0"].description  16.30hs 

			#([a-zA-Z0-9$&+,:;=?@#|'<>.^*()%!-/]+)
		]
		 
		for regular_expression, token_type in regular_expressions:
			m = re.search(regular_expression, document_word)
			if m != None:
				return token_type

		return "general"
			

	def increment_term_collection_frequency(self, term):
		if term in self.term_frequencies.keys():
			# Incremento la frecuencia de la colección
			self.term_frequencies[term][0] += 1
		else:
			# Inicializo con frecuencia de la colección en 1 y DF en 0
			self.term_length_acumulator += len(term)
			self.term_frequencies[term] = [1, 0]  


	def increment_document_frequency(self, document_terms):
		for term in document_terms:
			# Incremento la frecuencia en el documento
			self.term_frequencies[term][1] += 1

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Es necesario pasar los siguientes argumentos:')
		print('Obligatorio: Path al directorio de la coleccion')
		print("Opcional: Path al archivo de palabras vacias.")
		sys.exit(0)

	if len(sys.argv) == 3:
		empty_words_path = sys.argv[2]
	else:
		empty_words_path = None

	dirpath = sys.argv[1]

	import time
	start = time.time()
	ta = Tokenizer(dirpath, empty_words_path)
	end = time.time()
	print("\r\nExecution time: {} seconds.".format(end - start))

	#4.8, 5.62 segundos tiempo ejecución
