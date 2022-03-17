import sys
import pathlib
import re
import matplotlib.pyplot as plt


class Collection:
	def __init__(self, dirpath):
		self.dirpath = dirpath
		self.corpus_path = pathlib.Path(dirpath)
		self.documents = []
		self.process_documents()

	def process_documents(self):
		for file_path in self.corpus_path.iterdir():
			self.documents.append(Document(file_path))

	def get_document_count(self):
		return len(self.documents)

	def get_documents(self):
		return self.documents

	def get_shortest_document(self):
		shortest_document = self.documents[0]
		shortest_token_count = self.documents[0].get_token_count()
		for document in self.documents:
			if document.get_token_count() < shortest_token_count:
				shortest_document = document
				shortest_token_count = document.get_token_count()

		return shortest_document

	def get_longest_document(self):
		longest_document = self.documents[0]
		longest_token_count = self.documents[0].get_token_count()
		for document in self.documents:
			if document.get_token_count() > longest_token_count:
				longest_document = document
				longest_token_count = document.get_token_count()

		return longest_document

class Document:
	def __init__(self, path):
		self.path = path
		self.word_list = []
		self.parse_words()

	def parse_words(self):
		with open(self.path, "r") as f:
			for line in f.readlines():
				self.word_list.extend(line.strip().split())
	
	def get_words_list(self):
		return self.word_list

	def get_words_count(self):
		return len(self.word_list)

	def set_tokens(self, tokens):
		self.tokens = tokens
		self.token_count = len(tokens)
	
	def get_token_count(self):
		return self.token_count

	def get_path(self):
		print(self.path)

class Text_analyzer:

	def __init__(self, dirpath, delete_empty_words, empty_words_path):
		self.palabras_vacias = []

		if delete_empty_words == "True":
			with open(empty_words_path, "r") as f:
				for line in f.readlines():
					self.palabras_vacias.extend(line.split(","))

		self.collection = Collection(dirpath)

		self.term_file_path = "terminos.txt"
		self.statistics_file_path = "estadisticas.txt"
		self.frequencies_file_path = "frecuencias.txt"

	def generate_term_file(self):
		self.frequencies = self.obtain_frequencies()
		self.export_frequencies()

	def obtain_frequencies(self):
		frequencies = {}
		documents = self.collection.get_documents()

		for document in documents:
			document_word_list = document.get_words_list()
			
			document_tokens = []
			for document_word in document_word_list:
				if document_word not in self.palabras_vacias:
					document_tokens.append(document_word)
			document.set_tokens(document_tokens)
				
			frequencies = self.increment_frequency(frequencies, document_tokens)

		return frequencies
		
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

	

	def export_frequencies(self):
		sort_frequencies = sorted(self.frequencies.items(), key=lambda x: x[0])
		with open(self.term_file_path, "w") as f:
			for sort_frequency in sort_frequencies:
				f.write("{} {} {}".format(sort_frequency[0], sort_frequency[1][0], sort_frequency[1][1]))
				f.write("\r\n")

	def generate_statistics_file(self):
		with open(self.statistics_file_path, "w") as f:

			f.write(str(self.collection.get_document_count())+"\r\n")
			f.write(str(len(self.frequencies))+"\r\n")
			f.write(str(len(self.frequencies) / self.collection.get_document_count())+"\r\n")

			f.write(str(self.calculate_average_len_term())+"\r\n")
			
			f.write(str(self.collection.get_longest_document().get_token_count())+"\r\n")
			f.write(str(self.collection.get_shortest_document().get_token_count())+"\r\n")

			f.write(str(self.get_count_once_tokens())+"\r\n")

	def calculate_average_len_term(self):
		total_len = 0
		for frequency in self.frequencies:
			total_len += len(frequency)

		return total_len / len(self.frequencies)

	def get_count_once_tokens(self):
		counter = 0
		for frequency in self.frequencies:
			if self.frequencies[frequency][0] == 1:
				counter += 1
		return counter

	def generate_frequencies_file(self):
		sort_frequencies = sorted(self.frequencies.items(), key=lambda x: x[1][0])
		with open(self.frequencies_file_path, "w") as f:
			for frequent_frequency in sorted(sort_frequencies[-10:], key=lambda x:x[1][0], reverse=True):
				f.write(str("{} {}".format(frequent_frequency[0], frequent_frequency[1][0]))+"\r\n")

			f.write("\r\n")

			for non_frequent_frecuency in sort_frequencies[:10]:
				f.write(str("{} {}".format(non_frequent_frecuency[0], non_frequent_frecuency[1][0]))+"\r\n")
			


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
	ta.generate_term_file()
	ta.generate_statistics_file()
	ta.generate_frequencies_file()
