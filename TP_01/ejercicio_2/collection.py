import pathlib
from document import Document

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

	#def get_average_term_length(self):
		#for document in documents