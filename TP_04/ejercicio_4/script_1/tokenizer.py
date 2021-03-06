from normalizer import Normalizer
from bs4 import BeautifulSoup
from entity_extractor import Entity_Extractor
from constants import *


class Tokenizer:
    def __init__(self):
        self.inverted_index = {}

        self.palabras_vacias = []

        self.load_empty_words()

        self.normalizer = Normalizer(STEMMING_LANGUAGE)
        if EXTRACT_ENTITIES:
            self.entities_extractor = Entity_Extractor(STEMMING_LANGUAGE)

    def load_empty_words(self):
        if EMPTY_WORDS_PATH:
            with open(EMPTY_WORDS_PATH, "r") as f:
                for line in f.readlines():
                    self.palabras_vacias.append(line.strip())

    def valid_length(self, token):
        return len(token) >= MIN_TERM_LENGTH and len(token) <= MAX_TERM_LENGTH

    def palabra_vacia(self, token):
        for palabra_vacia in self.palabras_vacias:
            if palabra_vacia == token:
                return True
            if len(palabra_vacia) > len(token):
                return False
        return False

    def is_term(self, token):
        if not self.valid_length(token):
            return False
        if self.palabra_vacia(token):
            return False
        return True

    def add_term(self, term, doc_id):
        try:
            if doc_id not in self.inverted_index[term]:
                self.inverted_index[term].append(doc_id)
        except:
            self.inverted_index[term] = [doc_id]

    def add_if_term(self, token, file_id):
        if self.is_term(token):
            self.add_term(token, file_id)

    def tokenize_file(self, filename, file_id):
        with open(filename, "r", encoding=CORPUS_FILES_ENCODING) as f:
            for line in f.readlines():
                if EXTRACT_ENTITIES:
                    processed_line, entities = self.entities_extractor.extract_entities(
                        line
                    )
                    for entity in entities:
                        self.add_term(entity, file_id)
                else:
                    processed_line = line
                for word in processed_line.split():
                    token = self.normalizer.normalize(word)
                    self.add_if_term(token, file_id)

    def get_results(self):
        return self.inverted_index