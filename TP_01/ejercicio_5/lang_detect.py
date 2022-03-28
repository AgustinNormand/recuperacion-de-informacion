import pathlib
import sys
import re
import numpy as np
from nltk.stem import *
from sklearn.metrics import accuracy_score
from langdetect import detect

class LangDetect():
	def __init__(self, dirpath):
		self.path = pathlib.Path(dirpath)

		self.result = []

		self.process_test()

		self.solution = []

		self.read_solution()

		self.evaluate_model()


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

		with open(self.test_file_path, "r", encoding="Latin1") as f:
			for line in f.readlines():
				self.result.append(self.determine_language(line))
	
	def determine_language(self, line):
		lang_detected = detect(line)

		if lang_detected == "it":
			return "Italian"
		if lang_detected == "en":
			return "English"
		if lang_detected == "fr":
			return "French"
			
		return lang_detected


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Es necesario pasar los siguientes argumentos:')
		print('Obligatorio: Path al directorio de la coleccion')
		sys.exit(0)

	dirpath = sys.argv[1]

	ld = LangDetect(dirpath)
