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

	def get_token_count(self, token_type="all"):
		counter = 0
		for document in self.documents:
			counter += document.get_token_count(token_type)
		return counter

	def check_email_consistency(self):
		"""
		Verifico si la cantidad de @ del documento, coincide con la cantidad de tokens de email reconocidos.

		Como en muchos casos se encuentra la siguiente secuencia: @import
		En realidad verifico si la cantidad de @ del documento - (menos) la cantidad de @import, coincide con la cantidad de 
		tokens de email encontrados.
		"""

		for document in self.documents:
			import_count = count = document.get_file_content().count("@import")
			count = document.get_file_content().count("@")
			if (count - import_count) != len(document.get_email_tokens()):
				print("Diferente. Email token count:{}. Arroba ocurrences {}. File: {}. Email tokens: {}".format(
					len(document.get_email_tokens()), count, document.get_path(), document.get_email_tokens()))
				print("\r\n")
				print("\r\n")
				print("\r\n")

				# ...boletín oficial @import... No es email.
				# ...omitiendo @ y lo que le sigue...
				# ...oba username: @nexo.unnoba.edu.ar pass... ?
				# ...pción: seminarios07@unsam.edu.ar +info cursos de i... Faltaba agregar numeros en la RE
				# ...proyecto incluirt-@ el p...
				# ...twitter: @prensa_unsj...
				# ...itorial @import     ...

	def check_url_consistency(self):
		"""
		Inicialmente, verifico si la cantidaad de :// del documento, coincide con la cantidad de tokens url encontrados.
		Luego, verifico si la cantidad de www del documento coincide con la cantidad de tokens.
		"""

		for document in self.documents:
			patterns = ["://", "www"]
			for pattern in patterns:
				count = document.get_file_content().count(pattern)
				if count != document.get_token_count("url"):
					print("Diferente cantidad de "+pattern+" y urls detectadas. File: {}. URL tokens: {}".format(document.get_path(), document.get_tokens("url")))
					print("\r\n")

			# ... http://www.unsam.edu.ar/home/isa-vacaclonada-iib-inta-23junio2011-unsam.pdf ... Falaban guiones en RE
			# http://revistacyt.unne.edu.ar/noticia_bio7.php Faltabn guiones bajos
			# http://www.youtube.comhttp://www.youtube.com
			# www.unt.edu.ar/fcsnat/insue

class Document:
	def __init__(self, path):

		self.path = path
		self.word_list = []
		self.parse_words()

		self.token_dictionary = {}

		self.token_dictionary["all"] = []
		self.token_dictionary["email"] = []
		self.token_dictionary["general"] = []
		self.token_dictionary["number"] = []
		self.token_dictionary["url"] = []
		self.token_dictionary["abbreviation"] = []

	def parse_words(self):
		with open(self.path, "r") as f:
			for line in f.readlines():
				self.word_list.extend(line.strip().split())

	def get_words_list(self):
		return self.word_list

	def get_words_count(self):
		return len(self.word_list)

	def set_tokens(self, tokens):
		for token in tokens:
			self.token_dictionary["all"].append(token[0])
			self.token_dictionary[token[1]].append(token[0])

	def get_token_count(self, token_type="all"):
		return len(self.token_dictionary[token_type])

	def get_tokens(self, token_type="all"):
		return self.token_dictionary[token_type]

	def get_path(self):
		return self.path

	def get_file_content(self):
		with open(self.path, "r") as f:
			return f.read()

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
			document_word_list = document.get_words_list() ## Nombres propios

			document_tokens = []
			for document_word in document_word_list:
				if document_word not in self.palabras_vacias:

					document_token = [document_word,
									  self.get_token_type(document_word)]
					document_tokens.append(document_token)

			document.set_tokens(document_tokens)

			frequencies = self.increment_frequency(
				frequencies, document_tokens)

		return frequencies

	def get_token_type(self, document_word):
		regular_expressions = [
			["([a-zA-Z0-9]+@[a-z.]+)", "email"],
			["(https?://[a-zA-Z./0-9-_?=]+)", "url"],
			["([A-Z][a-z]+\.)", "abbreviation"], # Dr. Lic.
			["([A-Z]\.[A-Z]\.)", "abbreviation"], #S.A. #Este tiene que ir antes del de "etc."
			["([a-z]+\.)", "abbreviation"], # etc.
			["([A-Z]{4})", "abbreviation"], # NASA
			["([a-zA-Z]+[0-9]*[^A-Za-z0-9]*)", "general"], # Matcheo todo lo que no sea numeros
			["([0-9]+)", "number"], # Este no funcaba bien ( [0-9]+ ) matchea solo si tiene espacios adelante y atrás
			["([0-9]+\.[0-9]+)", "number"], # Decimales "(\b[0-9]+\.[0-9]+\b)"

			#([a-zA-Z0-9$&+,:;=?@#|'<>.^*()%!-/]+)
		]
		 
		for regular_expression, token_type in regular_expressions:
			m = re.search(regular_expression, document_word)
			if m != None:
				return token_type

		return "general"

	def increment_frequency(self, frequencies, document_tokens):
		unique_document_tokens = []
		for token, token_type in document_tokens:
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
				f.write("{} {} {}".format(
						sort_frequency[0], sort_frequency[1][0], sort_frequency[1][1]))
				f.write("\r\n")
				
		print("Archivo {} exportado.".format(self.term_file_path))

	def generate_statistics_file(self):
		with open(self.statistics_file_path, "w") as f:

			f.write(str(self.collection.get_document_count())+"\r\n")
			f.write(str(len(self.frequencies))+"\r\n")
			f.write(str(len(self.frequencies) /
						self.collection.get_document_count())+"\r\n")

			f.write(str(self.calculate_average_len_term())+"\r\n")

			f.write(
				str(self.collection.get_longest_document().get_token_count())+"\r\n")
			f.write(
				str(self.collection.get_shortest_document().get_token_count())+"\r\n")

			f.write(str(self.get_count_once_tokens())+"\r\n")
			print("Archivo {} exportado.".format(self.statistics_file_path))

			print("\r\n")
			print("----------------------------------------------------------------")
			print("Estadisticas de consola para debug")
			print("Document count {}.".format(self.collection.get_document_count()))
			print("Cantidad de tokens {}".format(len(self.frequencies)))
			print("Promedio de tokens de los docummentos {}.".format(len(self.frequencies) / self.collection.get_document_count()))
			print("Largo promedio de un termino {}.".format(self.calculate_average_len_term()))
			print("Cantidad de tokens del documento mas largo {}.".format(self.collection.get_longest_document().get_token_count()))
			print("Cantidad de tokens del documento mas corto {}.".format(self.collection.get_shortest_document().get_token_count()))
			print("Cantidad de terminos que aparecen solo 1 vez {}.".format(self.get_count_once_tokens()))
			
			print("Cantidad de tokens de tipo {}: {}".format("abbreviation", self.collection.get_token_count("abbreviation")))
			print("Cantidad de tokens de tipo {}: {}".format("email", self.collection.get_token_count("email")))
			print("Cantidad de tokens de tipo {}: {}".format("url", self.collection.get_token_count("url")))
			print("Cantidad de tokens de tipo {}: {}".format("number", self.collection.get_token_count("number")))

			print("Imprimiendo archivos de tokens")
			token_types = ["abbreviation", "email", "url", "number"]
			for token_type in token_types:
				with open("{}.txt".format(token_type), "w") as f:
					tokens = self.collection.get_tokens() # TODO

			#self.collection.save_token_files()
			#print(self.collection.get_token_count("url"))
			#print(self.collection.get_email_token_count())
			#self.collection.check_url_consistency()			

			
			print("----------------------------------------------------------------")
			print("\r\n")
			
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
		sort_frequencies = sorted(
			self.frequencies.items(), key=lambda x: x[1][0])
		with open(self.frequencies_file_path, "w") as f:
			for frequent_frequency in sorted(sort_frequencies[-10:], key=lambda x: x[1][0], reverse=True):
				f.write(
					str("{} {}".format(frequent_frequency[0], frequent_frequency[1][0]))+"\r\n")

			f.write("\r\n")

			for non_frequent_frecuency in sort_frequencies[:10]:
				f.write(str("{} {}".format(
						non_frequent_frecuency[0], non_frequent_frecuency[1][0]))+"\r\n")

		print("Archivo {} exportado.".format(self.frequencies_file_path))

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
