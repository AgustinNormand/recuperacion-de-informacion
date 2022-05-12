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

    ## Normalization

    def load_empty_words(self):
        if EMPTY_WORDS_PATH:
            with open(EMPTY_WORDS_PATH, "r") as f:
                for line in f.readlines():
                    self.palabras_vacias.append(line.strip())
    
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

    ##

    ## Cerca de 

    def get_doc_id(self, posting):
        return posting[0]

    def get_set_of_doc_ids(self, posting_list):
        result = set()
        for posting in posting_list:
            result.add(posting[0])
        return result

    def obtain_intersection(self, posting_list_1, posting_list_2):
        return self.get_set_of_doc_ids(posting_list_1).intersection(self.get_set_of_doc_ids(posting_list_2))

    def extraer_posiciones(self, doc_id, posting_list):
        for posting_list in posting_list:
            if self.get_doc_id(posting_list) == doc_id:
                return posting_list[2]

    def verificar_cercania(self, posiciones_term_1, posiciones_term_2):
        for posicion_term_1 in posiciones_term_1:
            for posicion_term_2 in posiciones_term_2:
                distance = posicion_term_1 - posicion_term_2
                if abs(distance) <= DISTANCIA_CERCANIA:
                    return True
        return False
    
    def near_query(self, term1, term2):
        results = []
        posting1 = self.importer.read_posting(term1, self.vocabulary)
        posting2 = self.importer.read_posting(term2, self.vocabulary)
        intersection = self.obtain_intersection(posting1, posting2)
        for doc_id in intersection:
            posiciones_term_1 = self.extraer_posiciones(doc_id, posting1)
            posiciones_term_2 = self.extraer_posiciones(doc_id, posting2)
            if self.verificar_cercania(posiciones_term_1, posiciones_term_2):
                results.append(doc_id)

        return results

    ##

    ## Next

    def verificar_contiguidad(self, posiciones_term_1, posiciones_term_2):
        for posicion_term_1 in posiciones_term_1:
            for posicion_term_2 in posiciones_term_2:
                distance = posicion_term_1 - posicion_term_2
                if distance == -1:
                    return True
        return False

    def next_query(self, term1, term2):
        results = []
        posting1 = self.importer.read_posting(term1, self.vocabulary)
        posting2 = self.importer.read_posting(term2, self.vocabulary)
        intersection = self.obtain_intersection(posting1, posting2)
        for doc_id in intersection:
            posiciones_term_1 = self.extraer_posiciones(doc_id, posting1)
            posiciones_term_2 = self.extraer_posiciones(doc_id, posting2)
            if self.verificar_contiguidad(posiciones_term_1, posiciones_term_2):
                results.append(doc_id)
        return results

    ##

    ## Frase

    def phrase_query(self, terms):
        acum_set = None
        #print(terms)
        for i in range(len(terms)-1):
            j = i+1
            #print("{} {}".format(i, j))
            near_query = "{} SIGUIENTE_A {}".format(terms[i], terms[j])
            #print(near_query)
            next_query_response = set(self.next_query(terms[i], terms[j]))
           #print(next_query_response)

            if acum_set == None:
                acum_set = next_query_response
            else:
                acum_set = acum_set.intersection(next_query_response)
            
        return acum_set

    ##

    def query(self, user_input):
        #print(self.vocabulary)
        if OPERADOR_CERCA in user_input:
            normalized_terms = self.normalize_terms(user_input.split(OPERADOR_CERCA))
            if len(normalized_terms) > 0:
                return self.near_query(*normalized_terms)
            else:
                return []
        if OPERADOR_SIGUIENTE in user_input:
            normalized_terms = self.normalize_terms(user_input.split(OPERADOR_SIGUIENTE))
            if len(normalized_terms) > 0:
                return self.next_query(*normalized_terms)
            else:
                return []
        if OPERADOR_FRASE in user_input:
            normalized_terms = self.normalize_terms(user_input.split(OPERADOR_FRASE)[1].split())
            if len(normalized_terms) > 0:
                return self.phrase_query(normalized_terms)
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

    ##

    def get_docnames_ids(self):
        return self.docnames_ids
