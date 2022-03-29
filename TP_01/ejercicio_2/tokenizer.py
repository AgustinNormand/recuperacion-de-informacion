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
		self.min_length = 0
		self.max_length = 200000

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

		test = []

		for document in documents:
			with open(document.get_path(), "r") as f:
				entities = {}
				document_lines = f.readlines()
				previous = None
				for i in range(0, len(document_lines)):
					if(i != len(document_lines)-1):
						further = document_lines[i+1]
					else:
						further = None

					self.process_line(entities, previous, document_lines[i], further)
					previous = document_lines[i]

				if entities != {}:
					print(document.get_path())
					print(entities)
					print("\r\n")
					for entity in entities["abbreviation4"]:
						if entity not in test:
							test.append(entity)
		print("Total len: {}".format(len(test)))

	def process_line(self, entities, previous_line, actual_line, further_line):
		regular_expressions = [
			#[r'(?:[A-Z][bcdfghj-np-tvxz]\.)|(?:[A-Z][a-z]{2}\.)', "abbreviation1"], #Dr. Lic.
			#[r'(?:\b[A-Z]\.[A-Z]\.[A-Z]\b)|(?:\b[A-Z]\.[A-Z]\.[A-Z]\.[A-Z]\b)|(?:\b[A-Z]\.[A-Z]\.)', "abbreviation2"], #U.S.A N.A.S.A S.A.
			#[r'(?:\b[A-Z]{2}\b)|(?:\b[A-Z]{3}\b)|(?:\b[A-Z]{4}\b)|(?:\b[A-Z]{5}\b)', "abbreviation3"],
			#[r'(?:\b[a-z]{3}\.\s)|(?:\s[a-z]{3}\.\s)', "abbreviation4"] # lic. nac. ing. dra. etc.
			#[r'(?:\b[a-z]{2}\.\s)|(?:\s[a-z]{2}\.\s)', "abbreviation4"] # dr. mg. sr. dr. ud.
		]

		for regular_expression, token_type in regular_expressions:
			""" 
			m = re.search(regular_expression, actual_line)
			if m != None:
				try:
					entities[token_type].append(m)
				except:
					entities[token_type] = [m]
			"""
			""" """
			m = re.findall(regular_expression, actual_line)
			if m != []:
				try:
					entities[token_type].extend(m)
				except:
					entities[token_type] = m
			""" """

	"""def get_token_type(self, document_word):
		regular_expressions = [
			["([A-Z][A-Z][A-Z])", "test"]
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
	"""
			

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
