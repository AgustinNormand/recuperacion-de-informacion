import pathlib
import sys
import re
import numpy as np
from nltk.stem import *
from sklearn.metrics import accuracy_score

class LangDetect():
	def __init__(self, dirpath):
		self.path = pathlib.Path(dirpath)

		self.train_filenames = ["English", "French", "Italian"]

		self.character_frequency = {}

		self.initialize_character_frequencies()

		self.result = []

		self.process_train_files()

		for key in self.character_frequency:
			print("{}: {}\r\n".format(key, self.character_frequency[key]))

		self.test_line_length = 0
		self.test_total_lines = 0

		self.process_test()

		self.solution = []

		self.read_solution()

		self.evaluate_model()

		print("Largo promedio de las lineas del conjunto de test: {}".format(self.test_line_length/self.test_total_lines))
		

	def evaluate_model(self):
		print("El accuracy del modelo es de {}".format(accuracy_score(self.solution, self.result)))
		error_count = 0
		total_count = 0
		right_count = 0
		for result, solution in zip(self.result, self.solution):
			total_count += 1
			if result != solution:
				error_count += 1
			else:
				right_count += 1

		print("La cantidad de acertados es de: {}".format(right_count))
		print("La cantidad de errados es de: {}".format(error_count))
		print("La cantidad total es de: {}".format(total_count))


	def read_solution(self):
		self.solution_file_path = self.path.joinpath("solution")
		with open(self.solution_file_path, "r", encoding="Latin1") as f:
			for line in f.readlines():
				self.solution.append(line.strip().split()[1])

	def process_test(self):
		self.test_file_path = self.path.joinpath("test")

		line_character_frequency = {}
		with open(self.test_file_path, "r", encoding="Latin1") as f:
			for line in f.readlines():
				self.test_total_lines += 1
				self.test_line_length += len(line)
				self.initialize_character_frequency(line_character_frequency)
				for word in line.strip().split():
					for letter in word:
						self.increment_frequency(line_character_frequency, letter.lower())
				self.result.append(self.determine_language(line_character_frequency))
	
	def determine_language(self, line_character_frequency):
		mayor = 0
		language = ""

		x = list(line_character_frequency.values())
		
		for train_filename in self.train_filenames:
			y = list(self.character_frequency[train_filename].values())
			corrcoef = np.corrcoef(x,y)[1][0]

			#if corrcoef == mayor:
			#	print("Warning")

			if corrcoef > mayor:
				mayor = corrcoef
				language = train_filename

		return language



	def process_train_files(self):
		self.train_path = self.path.joinpath("training")
		for filename in self.train_filenames:
			with open(self.train_path.joinpath(filename), "r", encoding="Latin1") as f:
				for line in f.readlines():
					for word in line.strip().split():
						for letter in word:
							self.increment_frequency(self.character_frequency[filename], letter.lower())

	def increment_frequency(self, character_frequency, key):
		try:
			character_frequency[key] += 1
		except:
			pass #Los que no son letras, van a entrar por aca.


	def initialize_character_frequency(self, character_frequency):
		for i in range(97,122):
			character_frequency[chr(i)] = 0

	def initialize_character_frequencies(self):
		for filename in self.train_filenames:
			self.character_frequency[filename] = {}
			self.initialize_character_frequency(self.character_frequency[filename])
			#for i in range(97,122):
				#self.character_frequency[filename][chr(i)] = 0

		



if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Es necesario pasar los siguientes argumentos:')
		print('Obligatorio: Path al directorio de la coleccion')
		sys.exit(0)

	dirpath = sys.argv[1]

	ld = LangDetect(dirpath)
