import re
from nltk.stem import SnowballStemmer

class Normalizer:
    def __init__(self, STEMMING_LANGUAGE):
        if STEMMING_LANGUAGE:
            self.stemming = True
            self.ps = SnowballStemmer(STEMMING_LANGUAGE)
        else:
            self.stemming = False

    def translate(self, to_translate):
        tabin = u'áäâàãéëèêẽíïìîóöòôúüùû'
        tabout = u'aaaaaeeeeeiiiioooouuuu'
        tabin = [ord(char) for char in tabin]
        translate_table = dict(zip(tabin, tabout))
        return to_translate.translate(translate_table)

    def remove_non_alphanumeric(self, result):
        return re.sub(r'[^a-zA-Z0-9]', '', result)

    def normalize(self, token):
        result = token.lower()
        result = self.translate(result)
        result = self.remove_non_alphanumeric(result)
        if self.stemming:
            result = self.ps.stem(result)
        return result

    def normalize_date(self, token):
        token = token.replace("/", "-")
        return token

    def normalize_abbreviation(self, token):
        result = token.lower()
        result = self.translate(result)
        result = self.remove_non_alphanumeric(result)
        return result
