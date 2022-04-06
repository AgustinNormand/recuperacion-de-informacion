import pathlib
from normalizer import Normalizer
from exporter import Exporter
#from collection import Collection
#from document import Document
#from exporter import Exporter

class Tokenizer:
	def __init__(self, vocabulary, documents_vectors, id_count):
		self.vocabulary = vocabulary
		self.documents_vectors = documents_vectors
		#self.documents_vectors = {}

		self.min_length = 2
		self.max_length = 20

		self.palabras_vacias = []
		#self.vocabulary = {} #TERMINO #idtermino #IDF 

		self.id_count = id_count

		self.load_empty_words("emptywords.txt")

		self.normalizer = Normalizer()

		


	def load_empty_words(self, empty_words_path):
		if empty_words_path:
			with open(empty_words_path, "r") as f:
				for line in f.readlines():
					self.palabras_vacias.append(line.strip())

	def valid_length(self, token): 
		return (len(token) > self.min_length and len(token) < self.max_length)

	def is_term(self, token):
		return token not in self.palabras_vacias and self.valid_length(token)

	"""def get_id(self, term):
		for index, term_info in self.vocabulary.items():
			if term_info[1] == term:
				return index
		return None

	def get_or_set_id_term(self, term):
		id_term = self.get_id(term)
		if id_term == None:
			self.vocabulary[self.id_count] = [0, term]
			id_term = self.id_count
			self.id_count += 1
		return id_term"""

	def increment_frequency(self, id_term, file_terms):
		try:
			file_terms[id_term] += 1
		except:
			file_terms[id_term] = 1

	def add_if_term(self, token, file_terms):
		if self.is_term(token):
			try:
				id_term = self.vocabulary[token][0]
			except:
				id_term = self.id_count.value
				self.vocabulary[token] = [id_term, 0]
				self.id_count.value += 1

			#id_term = self.get_or_set_id_term(token)
			self.increment_frequency(id_term, file_terms)

	def tokenize_file(self, filename, file_id):
		file_terms = {}
		with open(filename, "r") as f:
			for line in f.readlines():
				for word in line.strip().split():
					token = self.normalizer.normalize(word)
					self.add_if_term(token, file_terms)

		self.documents_vectors[file_id] = file_terms

	#def get_vocabulary(self):
		#return self.vocabulary