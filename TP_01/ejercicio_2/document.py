class Document:
	def __init__(self, path):

		self.path = path
		#self.word_list = []
		#self.parse_words()
		self.append_lines()

		self.token_list = []
		self.term_list = []

	"""def parse_words(self):
		with open(self.path, "r") as f:
			for line in f.readlines():
				self.word_list.extend(line.strip().split())"""
	def append_lines(self):
		with open(self.path, "r") as f:
			self.lines = f.readlines()

	def get_lines(self):
		return self.lines

	#def get_words_list(self):
		#return self.word_list

	#def get_words_count(self):
		#return len(self.word_list)

	def set_tokens(self, tokens):
		self.token_list.extend(tokens)

	def set_terms(self, terms):
		self.term_list.extend(terms)

	def get_token_count(self):
		return len(self.token_list)

	def get_term_count(self):
		return len(self.term_list)

	def get_path(self):
		return self.path