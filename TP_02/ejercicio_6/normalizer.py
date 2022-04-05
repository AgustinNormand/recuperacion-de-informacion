import re

class Normalizer:
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
