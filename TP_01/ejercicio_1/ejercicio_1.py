import sys
import matplotlib.pyplot as plt

from normalizer import Normalizer
from collection import Collection
from document import Document

class Text_analyzer:

	def __init__(self, dirpath, delete_empty_words, empty_words_path):
		self.palabras_vacias = []
		self.min_length = 0
		self.max_length = 10

		self.token_frequencies = {}
		self.terms = []

		self.load_empty_words()

		self.collection = Collection(dirpath)

		self.obtain_frequencies()

	def load_empty_words(self):
		if delete_empty_words == "True":
			with open(empty_words_path, "r") as f:
				for line in f.readlines():
					self.palabras_vacias.extend(line.split(","))

	def should_include_word(self, word): 
		if (len(word) > self.min_length and len(word) < self.max_length):
			return word not in self.palabras_vacias
		return False

	def obtain_frequencies(self):
		n = Normalizer()
		documents = self.collection.get_documents()

		for document in documents:
			document_word_list = document.get_words_list()

			document_tokens = []
			for document_word in document_word_list:
				if document_word not in self.palabras_vacias:
					document_token = n.normalize(document_word)
					
					document_tokens.append(document_token)

				#	if len(document_token) > self.min_length and len(document_token) < self.max_length:
				#		if document_token not in self.terms:
				#			self.terms.append(document_token)

				

			document.set_tokens(document_tokens)

			#self.token_frequencies = self.increment_frequency(
			#	self.token_frequencies, document_tokens)
			#print(self.token_frequencies)
		return self.token_frequencies

	def increment_frequency(self, frequencies, document_tokens):
		unique_document_tokens = []
		for token in document_tokens:
			if token not in unique_document_tokens:
				unique_document_tokens.append(token)
				if token in frequencies.keys():
					# Incremento la frecuencia en la colección
					frequencies[token][0] += 1
					# Incremento la frecuencia en el documento
					frequencies[token][1] += 1
				else:
					frequencies[token] = [1, 1]  # Inicializo ambas
			else:
				if token in frequencies.keys():
					# Incremento la frecuencia en la colección
					frequencies[token][0] += 1
				else:
					print("Warning: Entró a un if que no debería")

		return frequencies

	def increment_document_frequency(frequencies, tokens_list):
		document_words = []
		for token in tokens_list:
			if token not in document_words:
				document_words.append(token)
				if token in frequencies.keys():
					frequencies[token] += 1
				else:
					frequencies[token] = 1
		return frequencies



	

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('Es necesario pasar los siguientes argumentos:')
		print('Path a un directorio')
		print('True or False eliminar palabras vacias')
		sys.exit(0)

	empty_words_path = None
	if (sys.argv[2] == 'True'):
		if len(sys.argv) < 4:
			print('Indicar el Path al archivo de palabras vacias')
			sys.exit(0)
		else:
			empty_words_path = sys.argv[3]

	dirpath = sys.argv[1]
	delete_empty_words = sys.argv[2]

	ta = Text_analyzer(dirpath, delete_empty_words, empty_words_path)
