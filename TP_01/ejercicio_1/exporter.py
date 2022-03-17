	#def generate_term_file(self):
	#	self.frequencies = self.obtain_frequencies()
	#	self.export_frequencies()	
    
    	self.term_file_path = "terminos.txt"
		self.statistics_file_path = "estadisticas.txt"
		self.frequencies_file_path = "frecuencias.txt"

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


	def export_frequencies(self):
		sort_frequencies = sorted(self.frequencies.items(), key=lambda x: x[0])
		with open(self.term_file_path, "w") as f:
			for sort_frequency in sort_frequencies:
				f.write("{} {} {}\r\n".format(
						sort_frequency[0], sort_frequency[1][0], sort_frequency[1][1]))
				
		print("Archivo {} exportado.".format(self.term_file_path))

	
			
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