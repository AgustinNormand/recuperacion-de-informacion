			"""break
				try:
					if result["test"] != [None]:
						print(result["test"])
					except:
						pass
			break
				for line in f.readlines():
					self.evaluate_re(line)
					self.word_list.extend(line.strip().split())

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
			document.set_terms(unique_document_terms)"""


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