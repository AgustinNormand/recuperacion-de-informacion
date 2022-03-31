class Exporter:
	def __init__(self, term_frequencies, token_list, term_length_acumulator, entities, collection):
		self.collection = collection
		self.term_frequencies = term_frequencies
		self.term_length_acumulator = term_length_acumulator
		self.entities = entities

		self.token_list = token_list

		#Estos filenames no irian aca.
		self.term_file_path = "terminos.txt"
		self.statistics_file_path = "estadisticas.txt"
		self.frequencies_file_path = "frecuencias.txt"

	def generate_files(self):
		self.generate_term_file()
		self.generate_statistics_file()
		self.generate_frequencies_file()
		self.generate_entities_files()

	def generate_term_file(self):
		sort_frequencies = sorted(self.term_frequencies.items(), key=lambda x: x[0])
		with open(self.term_file_path, "w") as f:
			for sort_frequency in sort_frequencies:
				f.write("{} {} {}\r\n".format(
						sort_frequency[0], sort_frequency[1][0], sort_frequency[1][1]))
				
		print("Archivo {} exportado.".format(self.term_file_path))

	def generate_statistics_file(self):
		with open(self.statistics_file_path, "w") as f:

			### 1) Cantidad de documentos procesados
			document_count = self.collection.get_document_count()
			f.write("{}\r\n".format(document_count))
			###

			### 2) Cantidad de tokens y términos extraídos
			term_amount = len(self.term_frequencies.keys())
			token_amount = len(self.token_list)
			f.write("{} {}\r\n".format(token_amount, term_amount)) #Duda
			###

			### 3) Promedio de tokens y términos de los documentos
			f.write("{} {}\r\n".format(token_amount/document_count, term_amount/document_count))# Duda
			###

			### 4) Largo promedio de un término
			try:
				f.write("{}\r\n".format(self.term_length_acumulator / term_amount))
			except:
				f.write("{}\r\n".format(0))
			###

			### 5) Cantidad de tokens y términos del documento más corto y del más largo
			shortest_document = self.collection.get_shortest_document()
			token_count_shortest_document = shortest_document.get_token_count()
			term_count_shortest_document = shortest_document.get_term_count()

			longest_document = self.collection.get_longest_document()
			token_count_longest_document = longest_document.get_token_count()
			term_count_longest_document = longest_document.get_term_count()

			f.write("{} {} {} {}\r\n".format(token_count_shortest_document, term_count_shortest_document, token_count_longest_document, term_count_longest_document))
			###

			### 6) Cantidad de términos que aparecen sólo 1 vez en la colección
			f.write("{}\r\n".format(self.get_count_once_terms()))
			###

			print("Archivo {} exportado.".format(self.statistics_file_path))

	def get_count_once_terms(self):
		counter = 0
		for term_frequency in self.term_frequencies:
			if self.term_frequencies[term_frequency][0] == 1:
				counter += 1
		return counter
	
	def generate_frequencies_file(self):
		sort_frequencies = sorted(self.term_frequencies.items(), key=lambda x: x[1][0])
		with open(self.frequencies_file_path, "w") as f:
			for frequent_frequency in sorted(sort_frequencies[-10:], key=lambda x: x[1][0], reverse=True):
				f.write(
					str("{} {}".format(frequent_frequency[0], frequent_frequency[1][0]))+"\r\n")

			f.write("\r\n")

			for non_frequent_frecuency in sort_frequencies[:10]:
				f.write(str("{} {}".format(
						non_frequent_frecuency[0], non_frequent_frecuency[1][0]))+"\r\n")

		print("Archivo {} exportado.".format(self.frequencies_file_path))

			
	
	def generate_entities_files(self):
		try:
			with open("abbreviations.csv", "w") as f:
				for abbr in self.entities["abbreviation"]:
					f.write("{},\r\n".format(abbr.strip()))
		except:
			pass

		try:	
			with open("mails.csv", "w") as f:
				for mail in self.entities["mail"]:
					f.write("{},\r\n".format(mail.strip()))
		except:
			pass

		try:
			with open("urls.csv", "w") as f:
				for url in self.entities["url"]:
					f.write("{},\r\n".format(url.strip()))
		except:
			pass

		try:
			with open("numbers.csv", "w") as f:
				for number in self.entities["number"]:
					f.write("{},\r\n".format(number.strip()))
		except:
			pass

		try:
			with open("proper_names.csv", "w") as f:
				for proper_name in self.entities["proper_name"]:
					f.write("{},\r\n".format(proper_name.strip()))
		except:
			pass	

		"""
		print("\r\n")
			print("----------------------------------------------------------------")
			print("Estadisticas de consola para debug")
			print("Document count {}.".format(self.collection.get_document_count()))
			print("Cantidad de tokens {}".format(len(self.frequencies)))
			print("Promedio de tokens de los docummentos {}.".format(
				len(self.frequencies) / self.collection.get_document_count()))
			print("Largo promedio de un termino {}.".format(
				self.calculate_average_len_term()))
			print("Cantidad de tokens del documento mas largo {}.".format(
				self.collection.get_longest_document().get_token_count()))
			print("Cantidad de tokens del documento mas corto {}.".format(
				self.collection.get_shortest_document().get_token_count()))
			print("Cantidad de terminos que aparecen solo 1 vez {}.".format(
				self.get_count_once_tokens()))

			print("Cantidad de tokens de tipo {}: {}".format(
				"abbreviation", self.collection.get_token_count("abbreviation")))
			print("Cantidad de tokens de tipo {}: {}".format(
				"email", self.collection.get_token_count("email")))
			print("Cantidad de tokens de tipo {}: {}".format(
				"url", self.collection.get_token_count("url")))
			print("Cantidad de tokens de tipo {}: {}".format(
				"number", self.collection.get_token_count("number")))

			print("Imprimiendo archivos de tokens")
			token_types = ["abbreviation", "email", "url", "number"]
			for token_type in token_types:
				with open("{}.txt".format(token_type), "w") as f:
					tokens = self.collection.get_tokens()  # TODO

			# self.collection.save_token_files()
			# print(self.collection.get_token_count("url"))
			# print(self.collection.get_email_token_count())
			# self.collection.check_url_consistency()

			print("----------------------------------------------------------------")
			print("\r\n")
		"""