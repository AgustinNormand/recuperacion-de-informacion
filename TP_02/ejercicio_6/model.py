class Model:
	def __init__(self, vocabulary, document_vectors, docnames_ids, relevants = None):
		self.vocabulary = vocabulary
		self.document_vectors = document_vectors
		self.docnames_ids = docnames_ids

		#vocabulary = {id = term}
		#document_vectors = {id_doc = {id_term: cant, id_term: cant}}
		#docnames_ids = {id_doc = name}

		self.calculate_idf()

	"""def get_df(self, term_id):
		counter = 0
		for key in self.document_vectors:
			if term_id in list(self.document_vectors[key].keys()):
				counter += 1
		return counter
	"""
	def calculate_idf(self):
		for key in self.vocabulary:
			print(key)
			print(self.vocabulary[key])
			#self.get_df(key)
			break
			#break

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