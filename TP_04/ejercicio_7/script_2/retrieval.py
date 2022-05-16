import re
import struct

from importer import *
from normalizer import *
from entity_extractor import *

from constants import *


class Retrieval:
    def __init__(self, metadata, on_memory=False, avoid_sets=False, avoid_skips=False):
        self.metadata = metadata
        self.importer = Importer(metadata["TERMS_SIZE"], metadata["DOCNAMES_SIZE"])
        self.vocabulary = self.importer.read_vocabulary()
        self.ids_docnames = self.importer.read_docnames_ids_file()
        self.normalizer = Normalizer(metadata["STEMMING_LANGUAGE"])
        self.entity_extractor = Entity_Extractor(metadata["STEMMING_LANGUAGE"])

        self.avoid_sets = avoid_sets
        self.avoid_skips = avoid_skips

        self.on_memory = on_memory
        if self.on_memory:
            self.inverted_index = self.importer.read_inverted_index(self.vocabulary)

        ## Normalization

    def normalize_term(self, term):
        normalized_term = self.normalizer.normalize(term)
        return normalized_term

    def normalize_terms_without_entities(self, terms):
        normalized_terms = []
        for term in terms:
            normalized_term = self.normalize_term(term)
            normalized_terms.append(normalized_term)
        return normalized_terms

    def normalize_terms_with_entities(self, term):
        pass

    """

        if self.metadata["EXTRACT_ENTITIES"]:
            rest, entities_list = self.entity_extractor.extract_entities(term)
            if len(entities_list) >= 1:
                #if rest != "":?
                #if len(entities_list) >= 2: ?
                #if entity != term? #Doesnt work for U.S.A > usa
                entity = entities_list[0]
                return entity

        return self.normalizer.normalize(term)
        #Si tiene entidades que no estan en el vocabulary, intentar sin detectar la entidad.
    """

    def normalize_terms(self, terms):
        if self.metadata["EXTRACT_ENTITIES"]:
            # print("Pendiente")
            return self.normalize_terms_without_entities(terms)
        else:
            return self.normalize_terms_without_entities(terms)

    ##

    def query(self, user_input):
        ands = user_input.count(AND_SYMBOL)

        normalized_terms = self.normalize_terms(user_input.split(AND_SYMBOL))
        if not self.all_terms_in_vocabulary(normalized_terms):
            return []

        if (ands) == 1:
            if self.avoid_sets:
                if self.avoid_skips:
                    return self.and_query(normalized_terms)
                else:
                    return self.and_query_skips(normalized_terms)
            else:
                return sorted(list(self.and_query_sets(normalized_terms)))
        else:
            if self.avoid_sets:
                if self.avoid_skips:
                    return self.and_query(normalized_terms)
                else:
                    return self.and_query_skips(normalized_terms)
            else:
                return sorted(list(self.and_query_sets(normalized_terms)))

        return []

    ## Sets Querys

    def and_query_sets(self, terms):
        posting1 = self.get_posting(terms[0])
        posting2 = self.get_posting(terms[1])
        if len(terms) == 2:
            return set(posting1).intersection(set(posting2))
        else:
            posting3 = self.get_posting(terms[2])
            return set(posting1).intersection(set(posting2)).intersection(set(posting3))

    ##

    ## Handmade Querys

    def get_terms_in_order(self, terms):
        df_terms = {}
        for term in terms:
            df_term, _, _ = self.vocabulary[term]
            if df_term not in df_terms.keys():
                df_terms[df_term] = term
            else:
                df_terms[df_term] = [df_terms[df_term], term]

        terms_sorted_by_df = []
        for key in sorted(df_terms.keys()):
            if type(df_terms[key]) == list:
                terms_sorted_by_df.extend(df_terms[key])
            else:
                terms_sorted_by_df.append(df_terms[key])

        if len(terms_sorted_by_df) == 2:
            return terms_sorted_by_df[0], terms_sorted_by_df[1], None
        else:
            return terms_sorted_by_df[0], terms_sorted_by_df[1], terms_sorted_by_df[2]

    def search_with_skips(
        self, searching_doc_id, skips_term2, start_index_pointer, df_term
    ):
        previous_pointer = start_index_pointer
        for doc_id, pointer_index in skips_term2:
            if doc_id == searching_doc_id:
                return True
            if doc_id > searching_doc_id:
                for doc_id in self.importer.get_posting_part(previous_pointer, K_SKIPS):
                    if doc_id == searching_doc_id:
                        return True
                    if doc_id > searching_doc_id:
                        return False
            previous_pointer = pointer_index

        # Si salio del for, es porque todos los doc ids son menores, si está, esta al final.
        # La primera posicion que lee, es el valor de la posting, por eso 1 +
        return searching_doc_id in self.importer.get_posting_part(
            previous_pointer, 1 + (df_term % K_SKIPS)
        )

    def and_query_skips(self, terms):
        term1, term2, term3 = self.get_terms_in_order(terms)

        df_term2, skip_pointer_term2, index_pointer_term2 = self.vocabulary[term2]
        posting_term1 = self.get_posting(term1)
        skips_term2 = self.importer.get_skip(skip_pointer_term2, df_term2)

        two_term_result = self.two_term_and_query_skips(
            posting_term1, index_pointer_term2, skips_term2, df_term2
        )
        if term3 == None:
            return two_term_result
        else:
            if two_term_result == []:
                return []

            df_term3, skip_pointer_term3, index_pointer_term3 = self.vocabulary[term3]
            skips_term3 = self.importer.get_skip(skip_pointer_term3, df_term3)

            return self.two_term_and_query_skips(
                two_term_result, index_pointer_term3, skips_term3, df_term3
            )

    def two_term_and_query_skips(
        self, posting_term1, start_index_pointer_term2, skips_term2, df_term
    ):
        result = []
        for doc_id in posting_term1:
            found = self.search_with_skips(
                doc_id, skips_term2, start_index_pointer_term2, df_term
            )
            if found:
                result.append(doc_id)
        return result

    def search(
        self, searching_doc_id, posting
    ):
        for doc_id in posting:
            if doc_id == searching_doc_id:
                return True
            if doc_id > searching_doc_id:
                return False
        return False
    
    def and_query(self, terms):
        term1, term2, term3 = self.get_terms_in_order(terms)

        posting_term1 = self.get_posting(term1)
        posting_term2 = self.get_posting(term2)

        two_term_result = self.two_term_and_query(posting_term1, posting_term2)

        if term3 == None:
            return two_term_result
        else:
            if two_term_result == []:
                return []
            posting_term3 = self.get_posting(term3)
            return self.two_term_and_query(two_term_result, posting_term3)

    def two_term_and_query(
        self, posting_term1, posting_term2
    ):
        result = []
        for doc_id in posting_term1:
            found = self.search(
                doc_id, posting_term2
            )
            if found:
                result.append(doc_id)
        return result

    ##
    def get_posting(self, term):
        if self.on_memory:
            try:
                return self.inverted_index[term]
            except:
                if self.avoid_sets:
                    return []
                else:
                    return {}
        else:
            try:
                df_term, skips_pointer, index_pointer = self.vocabulary[term]
                return self.importer.read_posting(index_pointer, df_term)
            except:
                if self.avoid_sets:
                    return []
                else:
                    return {}

    def all_terms_in_vocabulary(self, terms):
        for term in terms:
            if term not in self.vocabulary.keys():
                return False
        return True

    def get_skip(self, term):
        try:
            normalized_term = self.normalize_term(term)
            df_term, skips_pointer, index_pointer = self.vocabulary[normalized_term]
            return self.importer.get_skip(skips_pointer, df_term)
        except:
            return []

    def get_vocabulary(self):
        return self.vocabulary.keys()
