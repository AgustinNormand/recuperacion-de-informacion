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
		self.min_length = 2
		self.max_length = 20

		self.term_frequencies = {}
		self.token_list = []

		self.term_length_acumulator = 0

		self.load_empty_words(empty_words_path)

		self.collection = Collection(dirpath)

		self.entities = {}

		self.normalizer = Normalizer()

		self.process_collection()

		##print(self.entities["date"])

		Exporter(self.term_frequencies, self.token_list, self.term_length_acumulator, self.entities, self.collection).generate_files()

	def load_empty_words(self, empty_words_path):
		if empty_words_path:
			with open(empty_words_path, "r") as f:
				for line in f.readlines():
					self.palabras_vacias.append(line.strip())

	def valid_length(self, token): 
		return (len(token) > self.min_length and len(token) < self.max_length)

	def is_term(self, token):
		return token not in self.palabras_vacias and self.valid_length(token)

	def process_collection(self):
		documents = self.collection.get_documents()
		
		for document in documents:
			document_entities = {}
			document_tokens = []
			unique_document_terms = []
			document_lines = document.get_lines()
			for i in range(0, len(document_lines)):
				processed_line = self.process_line(document_entities, document_lines[i])
				for document_word in processed_line.strip().split():

					document_token = self.normalizer.normalize(document_word)

					if document_token == "":
						continue
					
					document_tokens.append(document_token)

					self.token_list.append(document_token)

					is_valid_term = self.is_term(document_token)

					if is_valid_term:
						self.increment_term_collection_frequency(document_token)
						if document_token not in unique_document_terms:
							unique_document_terms.append(document_token)

			for key in document_entities:
				for document_entity in document_entities[key]:
					try:
						self.entities[key].append(document_entity)
					except:
						self.entities[key] = [document_entity]
					document_tokens.append(document_entity)
					self.token_list.append(document_entity)
					self.increment_term_collection_frequency(document_entity)
					if document_entity not in unique_document_terms:
						unique_document_terms.append(document_entity)

			self.increment_document_frequency(unique_document_terms)
			document.set_tokens(document_tokens)
			document.set_terms(unique_document_terms)

	def process_line(self, document_entities, actual_line):
		regular_expressions = [
			[r'(?:[0-9]{2}[\-/][0-9]{2}[\-/][0-9]{4})|(?:[0-9]{4}[\-/][0-9]{2}[\-/][0-9]{2})', "date"],
			[r'(\b[\w\.]+@[A-Za-z0-9\-]+\.[\.|A-Z|a-z]{2,}\b)', "mail"],
			[r'(?:[A-Z][bcdfghj-np-tvxz]\.)|(?:[A-Z][a-z]{2}\.)', "abbreviation"], #Dr. Lic.
			[r'([A-Z]{2}\.[A-Z]{2})', "abbreviation"], #EE.UU
			[r'(\b(?:[A-Z]\.?){2,})', "abbreviation"], #Poco checkeado. S.A S.A. U.S.A D.A.S.M.I N.A.S.A
			#[r'(?:\b[A-Z]\.[A-Z]\.[A-Z]\.[A-Z]\b)|(?:\b[A-Z]\.[A-Z]\.[A-Z]\b)|(?:\b[A-Z]\.[A-Z]\.)', "abbreviation"], #U.S.A N.A.S.A S.A.
			[r'(?:\b[A-Z]{2}\b)|(?:\b[A-Z]{3}\b)|(?:\b[A-Z]{4}\b)|(?:\b[A-Z]{5}\b)', "abbreviation"], #EJ FIFA USA
			[r'((?:\b[a-z]{2,3}\.\s)|(?:\s[a-z]{2,3}\.\s))', "abbreviation"], # lic. nac. ing. dra. etc.
			[r"((?:(?:https?://)|(?:www\.)|(?:ftps?://))(?:[a-zA-Z./0-9-_?=]+))", "url"],
			[r'((?:\b[0-9]+[\.,][0-9]+\b)|(?:\b[0-9]+\b))', "number"],
			[r'((?:(?:[A-ZÁÉÍÚÓ][a-záéíóú]+\s?){2,})|(?:(?!\A)[A-ZÁÉÍÚÓ][a-záéíóú]+))', "proper_name"], # El Quinto, Agustin Normand
		]
		##"abc.def@mail-archive.com"

		##https://docs.google.com/document/d/1ninD55Cfbb_7PksDirN0XghzNHJZ_N93lheQzF1aOZY/edit?usp=sharing

		for regular_expression, token_type in regular_expressions:
			m = re.findall(regular_expression, actual_line)
			actual_line = re.sub(regular_expression, "", actual_line)

			if re.findall(r"(U.S.A)", actual_line):
				print(re.findall(r"(\b(?:[A-Z]\.?){2,})", actual_line))
				#print(actual_line)

			if m != []:
				for value in m:
					#if token_type == "abbreviation":
						#if self.normalizer.normalize(value) in self.palabras_vacias:
							#continue
					try:
						document_entities[token_type].append(value.strip())
					except:
						document_entities[token_type] = [value.strip()]
		return actual_line


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

