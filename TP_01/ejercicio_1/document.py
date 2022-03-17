class Document:
	def __init__(self, path):

		self.path = path
		self.word_list = []
		self.parse_words()

		self.token_list = []
		self.term_list = []

	def parse_words(self):
		with open(self.path, "r") as f:
			for line in f.readlines():
				self.word_list.extend(line.strip().split())

	def get_words_list(self):
		return self.word_list

	def get_words_count(self):
		return len(self.word_list)

	def set_tokens(self, tokens):
		self.token_list.extend(tokens)

	#def get_token_count(self, token_type="all"):
	#	return len(self.token_dictionary[token_type])

	#def get_tokens(self, token_type="all"):
	#	return self.token_dictionary[token_type]

	def get_path(self):
		return self.path

	#def get_file_content(self):
	#	with open(self.path, "r") as f:
	#		return f.read()