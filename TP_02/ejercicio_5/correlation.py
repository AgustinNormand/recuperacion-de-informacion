import pathlib
import sys
import numpy as np
import math

def initialize(vector_dict, file_names):
	for file_name in file_names:
		vector_dict[str(file_name)] = {}
		for i in range(1, 6):
			vector_dict[str(file_name)][i] = []
	

def process_files(dirpath):
	files_dir = pathlib.Path(dirpath)

	retrieved_documents = {}
	initialize(retrieved_documents, files_dir.rglob("*.res"))
	for file_name in files_dir.rglob("*.res"):
		with open(file_name, 'r') as f:
			for line in f.readlines():
				query_number, _, doc_id, _, score, model = line.split()
				retrieved_documents[str(file_name)][int(query_number)].append([int(doc_id.split('d')[1]), score])
	
	return retrieved_documents
"""
def get_score(document_id, vector):
	for doc_id, score in vector:
		if document_id == doc_id:
			return score

	return 0
"""
def get_position(vector, value):
	return vector.index(value)

def spearman(vector1, vector2):
	acum = 0
	for i in range(len(vector1)):
		acum += pow(vector1[i]-vector2[i], 2)
	return acum

def calculate_correlations(retrieved_documents, query, count):
	file_keys = list(vector_dict.keys())

	vector_keys = {}

	

	for i in range(2):
		vector_keys[i] = []
		for doc_id, score in retrieved_documents[file_keys[i]][query]:
			vector_keys[i].append(doc_id)

	union = list(set(vector_keys[0][:count]).union(set(vector_keys[1][:count])))
	intersection = list(set(vector_keys[0][:count]).intersection(set(vector_keys[1][:count])))

	vectors = {}
	for i in range(2):
		vectors[i] = []
		for value in union:
			try:
				vectors[i].append(get_position(vector_keys[i], value))
			except:
				print("ERROR: Hay un documento que está en un ranking y en el otro no.")

	print("Primeros {} resultados".format(count))
	print(spearman(vectors[0], vectors[1]))

	"""
	unified_vectors = {}

	for i in range(2):
		vector = []
		for key in unique_doc_ids:
			vector.append(float(get_score(key, retrieved_documents[keys[i]][query])))

		unified_vectors[i] = vector
	#print("Corrcoef: {}".format(str(abs(np.corrcoef(unified_vectors[0], unified_vectors[1])[0][1])).replace(".", ",")))
	"""

	#print(retrieved_documents[keys[0]][1][:count])
	#print(unified_vectors[0])
	#print(retrieved_documents[keys[1]][1][:count])
	#print(unified_vectors[1])

if __name__ == '__main__':
	
	if len(sys.argv) < 2:
		print('Es necesario pasar como argumento un path a un directorio')
		sys.exit(0)

	dirpath = sys.argv[1]

	vector_dict = process_files(dirpath)

	for i in range(1, 6):
		print("Query: {}".format(i))
		calculate_correlations(vector_dict, i,10)
		#break
		calculate_correlations(vector_dict, i,25)
		calculate_correlations(vector_dict, i,50)
		print("\r\n")
	