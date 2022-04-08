import math
from tabulate import tabulate

class Model:
	def __init__(self, vocabulary, document_vectors, docnames_ids, relevants = None):
		self.vocabulary = vocabulary
		self.document_vectors = document_vectors
		self.docnames_ids = docnames_ids

		#print(document_vectors)

		#vocabulary = {term = [id, df, idf]}
		#document_vectors = {id_doc = {id_term: cant, id_term: cant}}
		#docnames_ids = {id_doc = name}

		self.documents_count = len(self.document_vectors.keys())
		self.calculate_idf()

		self.document_norm = {}

		self.calculate_documents_norm()

	def calculate_idf(self): ## Se podría refactorizar, Calcular antes.
		for key in self.vocabulary:
			self.vocabulary[key].append(math.log(self.documents_count/self.vocabulary[key][1]))

	def build_query_vector(self, query_terms):
		#Soportar multiple frecuencia en los terminos TODO
		self.query_vector = {}
		acum = 0
		for term in query_terms:
			try:
				term_idf = self.vocabulary[term][2]
				self.query_vector[term] = term_idf
				acum += math.pow(term_idf, 2)
			except:
				pass
		self.query_norm = math.sqrt(acum)
		self.query_terms_set = set(self.query_vector.keys())	

	def calculate_document_norm(self, document_vector):
		acum = 0
		for term in document_vector:
			tf = document_vector[term]
			idf = self.vocabulary[term][2]
			acum += math.pow(tf*idf, 2)

		return math.sqrt(acum)

	def calculate_documents_norm(self):
		for key in self.document_vectors:
			self.document_norm[key] = self.calculate_document_norm(self.document_vectors[key])

	def get_score(self, document_id, document_vector):
		document_terms_set = set(document_vector.keys())
		intersection = self.query_terms_set.intersection(document_terms_set)
		if len(intersection) != 0 :
			#print("document_id = {}, document_norm = {}".format(document_id, self.document_norm[document_id]))
			acum = 0
			for common_value in intersection:
				document_weight = document_vector[common_value] * self.vocabulary[common_value][2]
				query_weight = self.query_vector[common_value]
				acum += document_weight*query_weight
				#print("value = {}, doc_w = {}, query_w = {}".format(common_value, document_weight, query_weight))
				#print(common_value)
			try:
				return acum / (self.document_norm[document_id]*self.query_norm)
			except:
				return 0 #Esto estoy casi seguro que resuelve cuando el idf es 0
		else:
			return 0

	def get_document_scores(self):
		self.result = {}
		for key in self.document_vectors:
			score = self.get_score(key, self.document_vectors[key])
			if score != 0:
				self.result[key] = score
		#return result
				#print(score)
			#for common_term in intersection
		#print(result)
	
		#for term in self.query_vector:
			
	
	def query(self, query_terms):
		self.build_query_vector(query_terms)
		self.get_document_scores()

		final_ordered_result = []
		for value in self.result:
			doc_name = list(self.docnames_ids.keys())[list(self.docnames_ids.values()).index(value)]
			browser_path = "file:///home/agustin/Desktop/Recuperacion/repo/TP_02/ejercicio_6/"+doc_name
			final_ordered_result.append((value, self.result[value], browser_path))

		final_ordered_result = sorted(final_ordered_result, key=lambda tup: tup[1], reverse=True)

		print(tabulate(final_ordered_result, headers=['DocID', 'Score', 'DocPath'], tablefmt='orgtbl'))



"""term_documents = {}
document_terms = {}

for i in range(1, 203):
	term_documents[i] = []

for i in range(1, 39):
	document_terms[i] = []

with open("document_vector.txt", "r") as f:
	for line in f.readlines():
		doc_id, line = line.split(":")
		line = line.replace("(", "").replace(")", "")
		for number in line.split(","):
			term_documents[int(number.strip())].append(int(doc_id.strip()))
			document_terms[int(doc_id.strip())].append(int(number.strip()))

terms = {}

with open("vocabulary.txt", "r") as f:
	for line in f.readlines():
		id_term, idf, term = line.split("\t")
		terms[int(id_term)] = float(idf)


query_vector = {}
for i in range(1, 203):
	query_vector[i] = 0

raw_query = []
import sys
for term in sys.argv[2].split(","):
	query_vector[int(term)] = terms[int(term)]
	raw_query.append(int(term))

import math
def norma(vector):
	acum = 0
	for key in vector:
		acum += vector[key]*vector[key]
	return math.sqrt(acum)
	

document_vectors = {}
for i in range(1, 39):
	document_vectors[i] = {}
	for j in range(1, 203):
		if j in document_terms[i]:
			document_vectors[i][j] = terms[j]
		else:
			document_vectors[i][j] = 0


def scalar_product(vector1, vector2):
	acum = 0
	for i in range(1, 203):
		acum += vector1[i]*vector2[i]
	return acum


result = {}
for i in range(1, 39):
	sp = scalar_product(query_vector, document_vectors[i])
	qn = norma(query_vector)
	dn = norma(document_vectors[i])
	score = sp/(qn*dn)
	if score != 0:
		result[i] = score
		#print("Document {}, Score {}".format(i, result))

ordered_result = sorted(result.items(), key=lambda item: item[1], reverse=True)

relevant_docs = {}
for i in range(1, 6):
	relevant_docs[i] = []

with open("relevant_docs.txt", "r") as f:
	query_line = 1
	for line in f.readlines():
		for value in line.replace("(", "").replace(")", "").replace("\n", "").split(","):
			relevant_docs[query_line].append(int(value))
		query_line += 1

query_number = int(sys.argv[1])

final_ordered_result = []
#print(relevant_docs[1])

values_read = 0
relevants_count = 0
for value in ordered_result:
	relevant = ""
	values_read += 1	
	if value[0] in relevant_docs[query_number]:
		relevants_count += 1
		relevant = "x"
	final_ordered_result.append((value[0], value[1], relevants_count/values_read, relevants_count/len(relevant_docs[query_number]), relevant))
	#print(value)

#print("Query number {}, Query".format(query_number))
from tabulate import tabulate

info = [query_number, raw_query, relevant_docs[query_number]]
print(tabulate([info], headers=['Query Number', 'Query', "Relevants"], tablefmt='orgtbl'))

print("\r\n")

print("Retrived Documents:\r\n")

print(tabulate(final_ordered_result, headers=['DocID', 'Score', "Precision", "Recall", "Relevant"], tablefmt='orgtbl'))

"""