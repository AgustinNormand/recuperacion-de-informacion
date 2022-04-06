class Exporter:
	def __init__(self, docnames_ids, document_vectors, vocabulary):

		self.docnames_ids_file(docnames_ids, "./output/docnames_ids.txt")
		self.document_vectors_file(document_vectors, "./output/document_vectors.txt")
		self.vocabulary_file(vocabulary, "./output/vocabulary.txt")


	def docnames_ids_file(self, docnames_ids, filepath):
		with open(filepath, "w") as f:
			f.write("{}\t{}\r\n".format("doc_name", "id"))
			for doc_id in docnames_ids:
				f.write("{}\t{}\r\n".format(doc_id, docnames_ids[doc_id]))
	
	def document_vectors_file(self, document_vectors, filepath):
		with open(filepath, "w") as f:
			f.write("{}\t{}\r\n".format("doc_id", "{term_id: frecuency}"))
			for document_vector in document_vectors:
				f.write("{}\t{}\r\n".format(document_vector, document_vectors[document_vector]))

	def vocabulary_file(self, vocabulary, filepath):
		with open(filepath, "w") as f:
			f.write("{}\t{}\t{}\r\n".format("term_id", "IDF", 'term'))
			for value in vocabulary:
				f.write("{}\t{}\t{}\r\n".format(value, vocabulary[value][0], vocabulary[value][1]))