import pathlib
import sys
import re
from nltk.stem import *

class LangDetect():
	def __init__(self, dirpath):
		self.path = pathlib.Path(dirpath)

		self.train_path = self.path.joinpath("training")

		self.test_file_path = self.path.joinpath("test")

		self.train_filenames = ["English", "French", "Italian"]

		self.character_frequency = {}

		self.initialize_character_frequencies()

		self.process_train_files()

		for key in self.character_frequency:
			print("{}: {}\r\n".format(key, self.character_frequency[key]))

		self.process_test()

	def process_test(self):
		line_character_frequency = {}
		with open(self.test_file_path, "r", encoding="Latin1") as f:
			for line in f.readlines():
				self.initialize_character_frequency(line_character_frequency)
				for word in line.strip().split():
					for letter in word:
						self.increment_frequency(line_character_frequency, letter.lower())
				#print(line_character_frequency)


	def process_train_files(self):
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
