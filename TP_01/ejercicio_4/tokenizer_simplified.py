import pathlib
import sys
import re

class Tokenizer:
	def __init__(self, dirpath, empty_words_path):
		self.corpus_path = pathlib.Path(dirpath)
		self.documents = []

		self.load_empty_words(empty_words_path)

		self.process_collection()

	def load_empty_words(self, empty_words_path):
		if empty_words_path:
			with open(empty_words_path, "r") as f:
				for line in f.readlines():
					self.palabras_vacias.append(line.strip())

	def process_collection(self):
		for in_file in self.corpus_path.iterdir():
			with open(in_file, "r") as f:
				for line in f.readlines():
					tokens_list =  filter(lambda x: x not in self.palabras_vacias, [self.process(x) for x in line.strip().split()])

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
		result = self.normalize(token)
		result = self.stem(result)
		return result
	
	def stem(self, token):
		

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