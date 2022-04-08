from normalizer import Normalizer
from bs4 import BeautifulSoup

class Tokenizer:
	def __init__(self):
		self.documents_vectors = {}
		self.vocabulary = {}

		self.min_length = 2
		self.max_length = 20

		self.palabras_vacias = []

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

	def increment_frequency(self, term, file_terms):
		try:
			file_terms[term] += 1
		except:
			file_terms[term] = 1
			self.vocabulary[term] += 1

	def add_if_term(self, token, file_terms):
		if self.is_term(token):
			try:
				df = self.vocabulary[token]
			except:
				self.vocabulary[token] = 0

			self.increment_frequency(token, file_terms)

	def tokenize_html_file(self, filename, file_id):
		file_terms = {}
		with open(filename, 'r') as f:
			contents = f.read()
			soup = BeautifulSoup(contents, 'lxml')
			for word in soup.get_text().split():
				token = self.normalizer.normalize(word)
				self.add_if_term(token, file_terms)
		self.documents_vectors[file_id] = file_terms

	def get_results(self):
		return [self.vocabulary, self.documents_vectors]

	def tokenize_query(self, user_input):
		result = []
		for word in user_input.strip().split():
			token = self.normalizer.normalize(word)
			if self.is_term(token):
				result.append(token)
		return result