import pathlib
import sys
import numpy as np
import math

def initialize(vector_dict, file_names):
	for file_name in file_names:
		vector_dict[str(file_name)] = {}
		for i in range(1, 113):
			vector_dict[str(file_name)][i] = []
	

def process_files(dirpath):
	files_dir = pathlib.Path(dirpath)

	retrieved_documents = {}
	initialize(retrieved_documents, files_dir.rglob("*.res"))
	for file_name in files_dir.rglob("*.res"):
		with open(file_name, 'r') as f:
			for line in f.readlines():
				query_number, _, doc_id, _, score, model = line.split()
				retrieved_documents[str(file_name)][int(query_number)].append([int(doc_id), score])
	
	
	return retrieved_documents

def get_position(vector, value):
	return vector.index(value)

def sum_square(vector1, vector2):
	acum = 0
	for i in range(len(vector1)):
		acum += pow(vector1[i]-vector2[i], 2)
	return acum

def calculate_correlations(retrieved_documents, query):
	file_keys = list(vector_dict.keys())

	vector_keys = {}

	for i in range(2):
		vector_keys[i] = []
		for doc_id, score in retrieved_documents[file_keys[i]][query]:
			vector_keys[i].append(doc_id)

	for value in vector_keys[0]:
		if value not in vector_keys[1]:
			vector_keys[1].append(value)

	for value in vector_keys[1]:
		if value not in vector_keys[0]:
			vector_keys[0].append(value)

	union = set(vector_keys[0]).union(set(vector_keys[1]))

	vectors = {}
	for i in range(2):
		vectors[i] = []

	for value in list(union):
#		print("Document with id: {}".format(value))
		for i in range(2):
			position = get_position(vector_keys[i], value)
			#print("Position in {}, is: {}".format(i, position))
			vectors[i].append(position)


	k = len(vectors[0])
	denominador = (k*(pow(k,2)-1))/3
	return sum_square(vectors[0], vectors[1])/denominador

def get_ranking_size(retrieved_documents, query):
	file_keys = list(vector_dict.keys())

	vector_keys = {}

	for i in range(2):
		vector_keys[i] = []
		for doc_id, score in retrieved_documents[file_keys[i]][query]:
			vector_keys[i].append(doc_id)

	return len(set(vector_keys[0]).union(set(vector_keys[1])))

if __name__ == '__main__':
	
	if len(sys.argv) < 2:
		print('Es necesario pasar como argumento un path a un directorio')
		sys.exit(0)

	dirpath = sys.argv[1]

	vector_dict = process_files(dirpath)

	spearman_acumulator = 0
	size_acumulator = 0
	counter = 0
	for i in range(1, 113):
		size_acumulator += get_ranking_size(vector_dict, i)
		correlation = calculate_correlations(vector_dict, i)
		spearman_acumulator += correlation
		counter += 1

	print("Average size of spearman {}".format(spearman_acumulator/counter))

	print("Average size of rankings {}".format(size_acumulator/counter))
	