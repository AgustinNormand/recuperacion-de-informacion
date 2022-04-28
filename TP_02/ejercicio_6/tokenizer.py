from normalizer import Normalizer
from bs4 import BeautifulSoup


class Tokenizer:
    def __init__(self, empty_words_path):
        self.vocabulary = {}
        self.inverted_index = {}
        self.documents_vectors = {}

        self.min_length = 2
        self.max_length = 20

        self.palabras_vacias = []

        self.load_empty_words(empty_words_path)

        self.normalizer = Normalizer()

    def load_empty_words(self, empty_words_path):
        if empty_words_path:
            with open(empty_words_path, "r") as f:
                for line in f.readlines():
                    self.palabras_vacias.append(line.strip())

    def valid_length(self, token):
        return (len(token) > self.min_length and len(token) < self.max_length)

    def palabra_vacia(self, token):
        for palabra_vacia in self.palabras_vacias:
            if palabra_vacia == token:
                return True
            if len(palabra_vacia) > len(token):
                return False
        return False

    def is_term(self, token):
        return not self.palabra_vacia(token) and self.valid_length(token)

    def increment_inverted_index_frequency(self, term, file_id):
        try:
            added = False
            for i in range(len(self.inverted_index[term])):
                posting = self.inverted_index[term][i]

                if posting[0] == file_id:
                    self.inverted_index[term][i] = [posting[0], posting[1]+1]
                    added = True
                    break

            if not added:
                self.inverted_index[term].append([file_id, 1])

        except:
            self.inverted_index[term] = [[file_id, 1]]
            self.vocabulary[term] += 1

    def increment_file_terms_frequency(self, term, file_terms):
        try:
            file_terms[term] += 1
        except:
            file_terms[term] = 1

    def increment_frequency(self, term, file_id, file_terms):
        self.increment_inverted_index_frequency(term, file_id)
        self.increment_file_terms_frequency(term, file_terms)

    def add_if_term(self, token, file_id, file_terms):
        if self.is_term(token):
            try:
                df = self.vocabulary[token]
            except:
                self.vocabulary[token] = 0

            self.increment_frequency(token, file_id, file_terms)

    def tokenize_file(self, filename, file_id, html = False):
        file_terms = {}
        with open(filename, 'r') as f:
            contents = f.read()
            if html:
                soup = BeautifulSoup(contents, 'lxml')
                contents = soup.get_text()
            
            for word in contents.split():
                token = self.normalizer.normalize(word)
                self.add_if_term(token, file_id, file_terms)
        self.documents_vectors[file_id] = file_terms

    def get_results(self):
        return [self.vocabulary, self.inverted_index, self.documents_vectors]

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
