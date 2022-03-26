import pathlib
import sys
import re
from nltk.stem import *



class Tokenizer:
	def __init__(self, dirpath, empty_words_path):
		self.corpus_path = pathlib.Path(dirpath)
		self.documents = []

		self.load_empty_words(empty_words_path)

		self.lancasterStemmer = LancasterStemmer()
		self.porterStemmer = PorterStemmer()

		self.unique_words = []

		#self.totalWords = 0
		self.sameTreatedWords = 0
		self.differentTreatedWords = 0

		self.termsLancaster = []
		self.termsPorter = []

		self.process_collection()

		self.stem_unique_words()

		#print(len(self.unique_words))

	#	print("Cantidad tokens Lancaster:{}, Cantidad tokens Porter:{}".format(
	#		len(self.termsLancaster), len(self.termsPorter)))
		#print("TotalWords:{}, SameTreatedWords:{}, DifferentTreatedWords:{}".format(
		#	self.totalWords, self.sameTreatedWords, self.differentTreatedWords))

		#print("set(self.termsLancaster) - set(self.termsPorter)):{}".format(list(set(self.termsLancaster) - set(self.termsPorter))))

		#print("set(self.termsPorter) - set(self.termsLancaster)):{}".format(list(set(self.termsPorter) - set(self.termsLancaster))))

	def load_empty_words(self, empty_words_path):
		if empty_words_path:
			with open(empty_words_path, "r") as f:
				for line in f.readlines():
					self.palabras_vacias.append(line.strip())

	def process_collection(self):
		for in_file in self.corpus_path.iterdir():
			with open(in_file, "r") as f:
				for line in f.readlines():
					for word in line.strip().split():
						word = self.normalize(word)
						try:
							int(word)
						except:
							if word not in self.unique_words:
								self.unique_words.append(word)

	def stem_unique_words(self):
		for word in self.unique_words:
			lancasterStem = self.lancasterStemmer.stem(word)
			porterStem = self.porterStemmer.stem(word)
			if lancasterStem not in self.termsLancaster:
				self.termsLancaster.append(lancasterStem)

			if porterStem not in self.termsPorter:
				self.termsPorter.append(porterStem)

			if lancasterStem != porterStem:
				print("Word:{}, PorterStem:{}, LancasterStem:{}".format(word, porterStem, lancasterStem))
				self.differentTreatedWords += 1
			else:
				#print("Word:{}, PorterStem:{}, LancasterStem:{}".format(word, porterStem, lancasterStem))
				self.sameTreatedWords += 1

	def translate(self, to_translate):
		tabin = u'áéíóú'
		tabout = u'aeiou'
		tabin = [ord(char) for char in tabin]
		translate_table = dict(zip(tabin, tabout))
		return to_translate.translate(translate_table)

	def remove_non_alphanumeric(self, result):
		return re.sub(r'[^a-zA-Z0-9]', '', result)

	def normalize(self, token):
		result = token.lower()
		result = self.translate(result)
		result = self.remove_non_alphanumeric(result)
		return result

	def process(self, token):
		result = token
		#result = self.normalize(result)
		result = self.stem(result)
		return result

	# def stem(self, token):
	#	return self.stemmer.stem(token)


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Es necesario pasar los siguientes argumentos:')
		print('Obligatorio: Path al directorio de la coleccion')
		print("Opcional: Path al archivo de palabras vacias.")
		sys.exit(0)

	if len(sys.argv) == 3:
		empty_words_path = sys.argv[2]
	else:
		empty_words_path = None

	dirpath = sys.argv[1]

	import time
	start = time.time()
	ta = Tokenizer(dirpath, empty_words_path)
	end = time.time()
	print("\r\nExecution time: {} seconds.".format(end - start))
