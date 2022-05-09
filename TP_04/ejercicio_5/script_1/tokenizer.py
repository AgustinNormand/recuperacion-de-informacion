from constants import *

import sys

sys.path.append("../../ejercicio_1/script_1/")
from entity_extractor import Entity_Extractor
from normalizer import Normalizer


class Tokenizer:
    def __init__(self):
        self.vocabulary = {}
        self.inverted_index = {}
        #self.documents_vectors = {}
        self.index = {}
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

    def doc_id_present(self, term, doc_id):
        for stored_doc_id, _ in self.inverted_index[term]:
            if stored_doc_id == doc_id:
                return True
        return False

    def increment_frequency(self, term, doc_id):
        for value in self.inverted_index[term]:
            if value[0] == doc_id:
                value[1] += 1

    def increment_index_frequency(self, doc_id, term):
        try:
            self.index[doc_id][term] += 1
        except:
            self.index[doc_id][term] = 1

    def add_term(self, term, doc_id):
        self.increment_index_frequency(doc_id, term)
        if term not in self.inverted_index.keys():
            self.inverted_index[term] = [[doc_id, 1]]
            return

        if self.doc_id_present(term, doc_id):
            self.increment_frequency(term, doc_id)
        else:
            self.inverted_index[term].append([doc_id, 1])

    def add_if_term(self, token, doc_id):
        if self.is_term(token):
            self.add_term(token, doc_id)

    def increment_vocabulary(self, file_terms):
        for term in file_terms:
            try:
                self.vocabulary[term] += 1
            except:
                self.vocabulary[term] = 1

    def tokenize_file(self, filename, doc_id):
        self.index[doc_id] = {}
        with open(filename, "r", encoding=CORPUS_FILES_ENCODING) as f:
            for line in f.readlines():
                if EXTRACT_ENTITIES:
                    processed_line, entities = self.entities_extractor.extract_entities(
                        line
                    )
                    for entity in entities:
                        self.add_term(entity, doc_id)
                else:
                    processed_line = line
                for word in processed_line.split():
                    token = self.normalizer.normalize(word)
                    self.add_if_term(token, doc_id)
        self.increment_vocabulary(list(self.index[doc_id].keys()))

    def get_results(self):
        return [self.vocabulary, self.inverted_index, self.index]

    """
    def tokenize_query(self, user_input):
        result = {}
        for word in user_input.strip().split():
            token = self.normalizer.normalize(word)
            if self.is_term(token):
                try:
                    result[token] += 1
                except:
                    result[token] = 1
        return result

    def tokenize_posting(self, user_input):
        return Normalizer().normalize(user_input)
    """