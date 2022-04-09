import math
from tabulate import tabulate

class Model:
	def __init__(self, docnames_ids, vocabulary, inverted_index, documents_vectors, documents_norm):
		self.vocabulary = vocabulary
		self.inverted_index = inverted_index
		self.docnames_ids = docnames_ids
		self.documents_vectors = documents_vectors
		self.documents_norm = documents_norm

		#vocabulary = {term = [id, df, idf]}
		#document_vectors = {id_doc = {id_term: cant, id_term: cant}}
		#docnames_ids = {id_doc = name}


	def build_query_vector(self, query_terms):
		self.query_vector = {}
		acum = 0
		for term in query_terms:
			frequency = query_terms[term]
			try:
				term_idf = self.vocabulary[term][1]
				self.query_vector[term] = (1 + math.log(frequency)) * term_idf
				acum += math.pow(frequency * term_idf, 2)
			except:
				pass
		self.query_norm = math.sqrt(acum)
		#self.query_terms_set = set(self.query_vector.keys())	

		print("Vector de query: {}, Norma de la query: {}".format(self.query_vector, self.query_norm))

	def get_document_scores(self):
		self.scalar_product_acumulator = {}
		for term in self.query_vector:
			query_term_weight = self.query_vector[term]
			term_idf = self.vocabulary[term][1]
			for posting in self.inverted_index[term]:
				doc_id, document_tf = posting
				try:
					self.scalar_product_acumulator[doc_id] += query_term_weight * (document_tf * term_idf)
				except:
					self.scalar_product_acumulator[doc_id] = query_term_weight * (document_tf * term_idf)

		self.result = {}
		for doc_id in self.scalar_product_acumulator:
			try:
				score = self.scalar_product_acumulator[doc_id] / (self.query_norm * self.documents_norm[doc_id])
			except:
				score = 0
			if score != 0:
				self.result[doc_id] = score
	
			
	
	def query(self, query_terms):
		self.build_query_vector(query_terms)
		self.get_document_scores()
		
		final_ordered_result = []
		for value in self.result:
			doc_name = list(self.docnames_ids.keys())[list(self.docnames_ids.values()).index(value)]
			browser_path = "file:///home/agustin/Desktop/Recuperacion/repo/TP_02/ejercicio_6/"+doc_name
			final_ordered_result.append((value, self.result[value], browser_path))

		final_ordered_result = sorted(final_ordered_result, key=lambda tup: tup[1], reverse=True)
		
		print("\r\n")
		print(tabulate(final_ordered_result, headers=['DocID', 'Score', 'DocPath'], tablefmt='orgtbl'))

	def get_posting(self, term):
		try:
			return self.inverted_index[term]
		except:
			return None