from locale import normalize
from importer import Importer
from constants import *


import sys
sys.path.append("../script_1")
from entity_extractor import *
from normalizer import *


import math


class Retrieval:
    def __init__(self, metadata):
        self.metadata = metadata
        self.importer = Importer(metadata["TERMS_SIZE"], metadata["DOCNAMES_SIZE"])
        self.vocabulary = self.importer.read_vocabulary()
        self.normalizer = Normalizer(metadata["STEMMING_LANGUAGE"])
        self.entity_extractor = Entity_Extractor(metadata["STEMMING_LANGUAGE"])
        self.docnames_ids = self.importer.read_docnames_ids_file()
        self.palabras_vacias = []
        self.load_empty_words()

        #print(self.docnames_ids[771])

    def load_empty_words(self):
        if EMPTY_WORDS_PATH:
            with open(EMPTY_WORDS_PATH, "r") as f:
                for line in f.readlines():
                    self.palabras_vacias.append(line.strip())

    def get_doc_id(self, posting):
        return posting[0]

    # [771, 2, [1564, 2745]]
    def and_query(self, terms):
        self.terms_postings_lists = {}
        for term in terms:
            self.terms_postings_lists[term] = self.importer.read_posting(term, self.vocabulary)
        #print(self.terms_postings_lists)
        #Se podría hacer mejor con los punteros de las postings
        terms_docIds = {}
        for term in self.terms_postings_lists:
            for posting in self.terms_postings_lists[term]:
                try:
                    terms_docIds[term].add(self.get_doc_id(posting))
                except:
                    terms_docIds[term] = {self.get_doc_id(posting)}
        return list(set.intersection(*terms_docIds.values()))

    def obtener_posiciones(self, doc_id, term):
        for posting_list in self.terms_postings_lists[term]:
            if self.get_doc_id(posting_list) == doc_id:
                return posting_list[2]

    def substract(self, position_list, to_substract):
        #print(position_list)
        for i in range(len(position_list)):
            position_list[i] = position_list[i] - to_substract
        return set(position_list)

    def next_query(self, terms):
        print(terms)
        results = []
        intersection = self.and_query(terms)
        print(intersection)
        print(self.terms_postings_lists)
        docId_positions = {}
        for doc_id in intersection:
            position_list = []
            for term in terms:
                position_list.append(self.obtener_posiciones(doc_id, term))
                #print("{} {}".format(doc_id, term))
                #print(self.obtener_posiciones(doc_id, term))
                #print(self.terms_postings_lists[term])
            docId_positions[doc_id] = position_list
        #print(docId_positions)
        for doc_id in docId_positions:
            set_positions_lists = []
            positions_lists = docId_positions[doc_id]
            to_substract = 0
            for position_list in positions_lists:
                set_position_list = self.substract(position_list, to_substract)
                to_substract += 1
                set_positions_lists.append(set_position_list)
            #print(doc_id)
            #print(set_positions_lists)
            if set.intersection(*(set_positions_lists)) != set():
                results.append(doc_id)
        return results

    def normalize_terms_without_entities(self, terms):
        normalized_terms = []
        for term in terms:
            normalized_term = self.normalizer.normalize(term)
            if not self.palabra_vacia(normalized_term):
                if normalized_term not in self.vocabulary.keys():
                    return []
                else:
                    normalized_terms.append(normalized_term)
        return normalized_terms

    def normalize_terms(self, terms):
        if self.metadata["EXTRACT_ENTITIES"]:
            print("Pendiente")
            return self.normalize_terms_without_entities(terms)
        else:
            return self.normalize_terms_without_entities(terms)

    def palabra_vacia(self, token):
        for palabra_vacia in self.palabras_vacias:
            if palabra_vacia == token:
                return True
            if len(palabra_vacia) > len(token):
                return False
        return False

    def near_query(self, terms):
        intersection = self.and_query(terms)
        #print(intersection)

    def query(self, user_input):
        #print(self.vocabulary)
        if OPERADOR_CERCA in user_input:
            normalized_terms = self.normalize_terms(user_input.split(OPERADOR_CERCA))
            if len(normalized_terms) > 0:
                return self.near_query()
            else:
                return []
        if OPERADOR_SIGUIENTE in user_input:
            normalized_terms = self.normalize_terms(user_input.split(OPERADOR_SIGUIENTE))
            if len(normalized_terms) > 0:
                return self.next_query(normalized_terms)
            else:
                return []
        if OPERADOR_FRASE in user_input:
            normalized_terms = self.normalize_terms(user_input.split(OPERADOR_FRASE)[1].split())
            if len(normalized_terms) > 0:
                return self.next_query(normalized_terms)
            else:
                return []

    ## TEST RESULTS
    def get_posting(self, term):
        if self.metadata["EXTRACT_ENTITIES"]:
            rest, entities_list = self.entity_extractor.extract_entities(term)
            if len(entities_list) >= 1:
                entity = entities_list[0]
                processed_term = entity
            else:
                processed_term = self.normalizer.normalize(term)
        else:
            processed_term = self.normalizer.normalize(term)

        postings_lists = self.importer.read_posting(processed_term, self.vocabulary)

        return postings_lists

    def get_vocabulary(self):
        return self.vocabulary

    def get_vocabulary_value(self, term):
        if self.metadata["EXTRACT_ENTITIES"]:
            rest, entities_list = self.entity_extractor.extract_entities(term)
            if len(entities_list) >= 1:
                entity = entities_list[0]
                processed_term = entity
            else:
                processed_term = self.normalizer.normalize(term)
        else:
            processed_term = self.normalizer.normalize(term)
        return self.vocabulary[processed_term]
