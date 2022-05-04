from normalizer import Normalizer
from bs4 import BeautifulSoup
from entity_extractor import Entity_Extractor
import constants as c


class Tokenizer:
    def __init__(self):
        self.vocabulary = {}
        self.inverted_index = {}
        self.documents_vectors = {}

        self.palabras_vacias = []

        self.load_empty_words()

        self.normalizer = Normalizer()
        if c.EXTRACT_ENTITIES:
            self.entities_extractor = Entity_Extractor()

    def load_empty_words(self):
        if c.EMPTY_WORDS_PATH:
            with open(c.EMPTY_WORDS_PATH, "r") as f:
                for line in f.readlines():
                    self.palabras_vacias.append(line.strip())

    def valid_length(self, token):
        return len(token) > c.MIN_TERM_LENGTH and len(token) < c.MAX_TERM_LENGTH

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

    def add_term(self, term, doc_id, file_terms):
        try:
            if doc_id not in self.inverted_index[term]:
                self.inverted_index[term].append(doc_id)
        except:
            self.inverted_index[term] = [doc_id]

        if term not in file_terms:
            file_terms.append(term)

    def add_if_term(self, token, file_id, file_terms):
        if self.is_term(token):
            self.add_term(token, file_id, file_terms)

    def increment_vocabulary(self, file_terms):
        for term in file_terms:
            try:
                self.vocabulary[term] += 1
            except:
                self.vocabulary[term] = 1
            
    def tokenize_html_file(self, filename, file_id):
        file_terms = []
        with open(filename, "r") as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            content = soup.get_text().replace("\n", "").replace("\xa0", "")
            if c.EXTRACT_ENTITIES:
                processed_content, entities = self.entities_extractor.extract_entities(
                            content
                        )
                for entity in entities:
                    self.add_term(entity, file_id, file_terms)
            else:
                processed_content = content

            for word in processed_content.split():
                token = self.normalizer.normalize(word)
                self.add_if_term(token, file_id, file_terms)
        self.increment_vocabulary(file_terms)

    def tokenize_file(self, filename, file_id):
        if c.HTML_FILES:
            self.tokenize_html_file(filename, file_id)
        else:
            file_terms = []
            with open(filename, "r") as f:
                for line in f.readlines():
                    if c.EXTRACT_ENTITIES:
                        processed_line, entities = self.entities_extractor.extract_entities(
                            line
                        )
                        for entity in entities:
                            self.add_term(entity, file_id, file_terms)
                    else:
                        processed_line = line
                    for word in processed_line.split():
                        token = self.normalizer.normalize(word)
                        self.add_if_term(token, file_id, file_terms)

            self.increment_vocabulary(file_terms)

    def get_results(self):
        return [self.vocabulary, self.inverted_index]

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
