import pathlib
import sys
import numpy as np

def initialize(vector_dict, file_names):
	for file_name in file_names:
		vector_dict[str(file_name)] = {}
		for i in range(1, 6):
			vector_dict[str(file_name)][i] = []
	

def process_files(dirpath):
	files_dir = pathlib.Path(dirpath)

	vector_dict = {}
	initialize(vector_dict, files_dir.rglob("*.res"))
	for file_name in files_dir.rglob("*.res"):
		with open(file_name, 'r') as f:
			for line in f.readlines():
				query_number, _, doc_id, _, score, model = line.split()
				#print(score)
				#vector_dict[str(file_name)][int(query_number)].append(float(score))
				vector_dict[str(file_name)][int(query_number)].append(int(doc_id.split('d')[1]))
	return vector_dict


def calculate_correlations(vector_dict):
	keys = list(vector_dict.keys())
	#print(vector_dict[keys[0]][1][:5])
	#print(vector_dict[keys[1]][1][:5])

	for i in range(1, 6):
		print("Query {}".format(i))
		print("Correlation first 10")
		print(str(np.corrcoef(vector_dict[keys[0]][i][:10], vector_dict[keys[1]][i][:10])[0][1]).replace(".", ","))

		print("Correlation first 25")
		print(str(np.corrcoef(vector_dict[keys[0]][i][:25], vector_dict[keys[1]][i][:25])[0][1]).replace(".", ","))

		print("Correlation first 50")
		print(str(np.corrcoef(vector_dict[keys[0]][i][:50], vector_dict[keys[1]][i][:50])[0][1]).replace(".", ","))

		print("\r\n")

if __name__ == '__main__':
	
	if len(sys.argv) < 2:
		print('Es necesario pasar como argumento un path a un directorio')
		sys.exit(0)

	dirpath = sys.argv[1]

	vector_dict = process_files(dirpath)

	calculate_correlations(vector_dict)
	