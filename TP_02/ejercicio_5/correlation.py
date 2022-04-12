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

def get_score(document_id, vector):
	for doc_id, score in vector:
		if document_id == doc_id:
			return score

	return 0

def calculate_correlations(retrieved_documents, query, count):
	keys = list(vector_dict.keys())
	#query = 1
	#count = 5
	unique_doc_ids = []

	print("Query: {}".format(query))

	for i in range(2):
		for doc_id, score in retrieved_documents[keys[i]][query][:count]:
			if doc_id not in unique_doc_ids:
				unique_doc_ids.append(doc_id)

	print("Primeros {} resultados".format(count))
	#print("Vector keys: {}".format(unique_doc_ids))

	unified_vectors = {}

	for i in range(2):
		vector = []
		for key in unique_doc_ids:
			vector.append(float(get_score(key, retrieved_documents[keys[i]][query])))

		unified_vectors[i] = vector
	print("Corrcoef: {}".format(str(abs(np.corrcoef(unified_vectors[0], unified_vectors[1])[0][1])).replace(".", ",")))

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
		calculate_correlations(vector_dict, i,10)
		calculate_correlations(vector_dict, i,25)
		calculate_correlations(vector_dict, i,50)
		print("\r\n")
	