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

def get_position(vector, value):
	return vector.index(value)

def sum_square(vector1, vector2):
	acum = 0
	for i in range(len(vector1)):
		acum += pow(vector1[i]-vector2[i], 2)
	return acum

def calculate_correlations(retrieved_documents, query, count):
	file_keys = list(vector_dict.keys())

	vector_keys = {}

	for i in range(2):
		vector_keys[i] = []
		for doc_id, score in retrieved_documents[file_keys[i]][query][:count]:
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

	print("Primeros {} resultados".format(count))
	print(vector_keys[0])
	print(vector_keys[1])
	#print(vectors[0])
	#print(vectors[1])
	k = len(vectors[0])
	denominador = (k*(pow(k,2)-1))/3
	return sum_square(vectors[0], vectors[1])/denominador

if __name__ == '__main__':
	
	if len(sys.argv) < 2:
		print('Es necesario pasar como argumento un path a un directorio')
		sys.exit(0)

	dirpath = sys.argv[1]

	vector_dict = process_files(dirpath)

	#file_keys = list(vector_dict.keys())
	#print([x[0] for x in vector_dict[file_keys[0]][1][:10]])
	#print([x[0] for x in vector_dict[file_keys[1]][1][:10]])

	print(calculate_correlations(vector_dict, 1,10))

	#for i in range(1, 6):
		#print("Query: {}".format(i))
		#print(calculate_correlations(vector_dict, i,10))
		#break
		#calculate_correlations(vector_dict, i,25)
		#calculate_correlations(vector_dict, i,50)
		#print("\r\n")
	