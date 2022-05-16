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
        #if normalized_term not in self.vocabulary.keys():
        #    return None
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

    ## Sets Querys

    def and_query_sets(self, terms):
        posting1 = self.get_posting(terms[0])
        posting2 = self.get_posting(terms[1])
        if len(terms) == 2:
            return set(posting1).intersection(set(posting2))
        else:
            posting3 = self.get_posting(terms[2])
            return set(posting1).intersection(set(posting2)).intersection(set(posting3))

    """
    def or_query_sets(self, terms):
        posting1 = self.get_posting(terms[0])
        posting2 = self.get_posting(terms[1])
        return set(posting1).union(set(posting2))

    def not_query_sets(self, terms):
        posting1 = self.get_posting(terms[0])
        posting2 = self.get_posting(terms[1])
        return set(posting1).difference(set(posting2))
    """

    def one_operator_query_sets(self, normalized_terms, ands, ors, nots):
        if ands == 1:
            return sorted(list(self.and_query_sets(normalized_terms)))
        """
        if ors == 1:
            return sorted(list(self.or_query_sets(normalized_terms)))
        if nots == 1:
            return sorted(list(self.not_query_sets(normalized_terms)))
        """

    def two_operator_query_sets(self, user_input, ands, ors, nots):
        if ands == 2:
            normalized_terms = self.normalize_terms(user_input.split(AND_SYMBOL))
            if not self.all_terms_in_vocabulary(normalized_terms):
                return []
            else:
                return sorted(list(self.and_query_sets(normalized_terms)))

        parenthesis = re.findall(r"\((.*?)\)", user_input)[0]
        parenthesis_resultset = set(self.query(parenthesis))
        rest = user_input.replace("(" + parenthesis + ")", "")
        if AND_SYMBOL in rest:
            normalized_term = self.normalize_term(rest.replace(AND_SYMBOL, ""))
            if normalized_term in self.vocabulary.keys():
                return sorted(list(set(self.get_posting(normalized_term)).intersection(parenthesis_resultset)))
            else:
                return []
        """
        if NOT_SYMBOL in rest:
            normalized_term = self.normalize_term(rest.replace(NOT_SYMBOL, ""))
            return sorted(list(parenthesis_resultset.difference(set(self.get_posting(normalized_term)))))

        if OR_SYMBOL in rest:
            normalized_term = self.normalize_term(rest.replace(OR_SYMBOL, ""))
            return sorted(list(parenthesis_resultset.union(set(self.get_posting(normalized_term)))))
        """
    ##

    ## Handmade Querys
    """
    def or_query(self, posting1, posting2):
        pointer1 = 0
        pointer2 = 0

        if pointer1 == len(posting1):
                pointer1 = None

        if pointer2 == len(posting2):
            pointer2 = None

        results = []

        while (pointer1 != None) or (pointer2 != None):
            if pointer1 != None and pointer2 != None:
                # Ambas listas todavía tienen elementos
                element1 = posting1[pointer1]
                element2 = posting2[pointer2]

                if element1 == element2:
                    results.append(element1)
                    pointer1 += 1
                    pointer2 += 1
                
                if element1 > element2:
                    results.append(element2)
                    pointer2 += 1

                if element2 > element1:
                    results.append(element1)
                    pointer1 += 1

            if pointer1 != None and pointer2 == None:
                results.append(posting1[pointer1])
                pointer1 += 1

            if pointer1 == None and pointer2 != None:
                results.append(posting2[pointer2])
                pointer2 += 1
            
            if pointer1 == len(posting1):
                pointer1 = None

            if pointer2 == len(posting2):
                pointer2 = None

        return results
    def find(self, doc_id, posting, index_list):
        for index in index_list:
            if posting[index] == doc_id:
                index_list.remove(index)
                return True
            if posting[index] > doc_id:
                return False
        return False

    def not_query(self, posting1, posting2):
        results = []

        index_list = list(range(len(posting2)))
        
        for doc_id in posting1:
            if not self.find(doc_id, posting2, index_list):
                results.append(doc_id)
        return results
    """

    def two_term_and_query(self, posting_term1, start_index_pointer_term2, skips_term2, df_term):
        result = []
        # print("Posting of short df term: {}".format(posting_term1))
        # print("Skips of other term: {}".format(skips_term2))
        # print("Start in index pointer: {}".format(start_index_pointer_term2))
        #print(posting_term1)
        #print(skips_term2)
        for doc_id in posting_term1:
            #print(doc_id)
            found = self.search_with_skips(
                doc_id, skips_term2, start_index_pointer_term2, df_term
            )
            if found:
                result.append(doc_id)
            #print("{} {}".format(doc_id, found))
        return result

    def one_operator_query(self, normalized_terms, ands, ors, nots):
        #print("{} Ands:{} Ors:{} Nots:{}".format(normalized_terms, ands, ors, nots))
        if ands == 1:
            if self.avoid_skips:
            return self.and_query(normalized_terms)
        """
        posting1 = self.get_posting(normalized_terms[0])
        posting2 = self.get_posting(normalized_terms[1])

        if ors == 1:
            return self.or_query(posting1, posting2)
        if nots == 1:
            return self.not_query(posting1, posting2)
        """

    def two_operator_query(self, user_input, ands, ors, nots):
        if ands == 2:
            normalized_terms = self.normalize_terms(user_input.split(AND_SYMBOL))
            if not self.all_terms_in_vocabulary(normalized_terms):
                return []
            else:
                return self.and_query(normalized_terms)

        parenthesis = re.findall(r"\((.*?)\)", user_input)[0]
        parenthesis_resultset = self.query(parenthesis)
        rest = user_input.replace("(" + parenthesis + ")", "")

        if AND_SYMBOL in rest:
            #print(user_input)

            normalized_term = self.normalize_term(rest.replace(AND_SYMBOL, ""))
            if normalized_term in self.vocabulary.keys():
                df_term, skips_pointer, index_pointer = self.vocabulary[normalized_term]
                #print(self.vocabulary[normalized_term])
                skips = self.importer.get_skip(skips_pointer, df_term)
                #print(skips)
                return self.two_term_and_query(parenthesis_resultset, index_pointer, skips, df_term)
            else:
                return []
        """
        if NOT_SYMBOL in rest:
            normalized_term = self.normalize_term(rest.replace(NOT_SYMBOL, ""))
            return self.not_query(parenthesis_resultset, self.get_posting(normalized_term))

        if OR_SYMBOL in rest:
            normalized_term = self.normalize_term(rest.replace(OR_SYMBOL, ""))
            return self.or_query(parenthesis_resultset, self.get_posting(normalized_term))
        """
    ##

    def query(self, user_input):
        ands = user_input.count(AND_SYMBOL)
        ors = user_input.count(OR_SYMBOL)
        nots = user_input.count(NOT_SYMBOL)

        if (ands + ors + nots) == 1:
            if ands == 1:
                normalized_terms = self.normalize_terms(user_input.split(AND_SYMBOL))
                if not self.all_terms_in_vocabulary(normalized_terms):
                    return []
            if ors == 1:
                normalized_terms = self.normalize_terms(user_input.split(OR_SYMBOL))
            if nots == 1:
                normalized_terms = self.normalize_terms(user_input.split(NOT_SYMBOL))

            if normalized_terms == []:
                return []

            if self.avoid_sets:
                return self.one_operator_query(normalized_terms, ands, ors, nots)
            else:
                return self.one_operator_query_sets(normalized_terms, ands, ors, nots)
        else:
            if (ands + ors + nots) > 1:
                if self.avoid_sets:
                    return self.two_operator_query(user_input, ands, ors, nots)
                else:
                    return self.two_operator_query_sets(user_input, ands, ors, nots)

        return []

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
    """
    

    def get_index_pointer(self, term):
        try:
            df_term, skips_pointer, index_pointer = self.vocabulary[term]
            return index_pointer
        except:
            return None
    """

    

    def and_query(self, terms):
        #print(terms)
        df_terms = {}
        for term in terms:
            df_term, _, _ = self.vocabulary[term]
            if df_term not in df_terms.keys():
                df_terms[df_term] = term
            else:
                # Dos términos tienen el mismo DF
                df_terms[df_term] = [df_terms[df_term], term]

        #print(df_terms)

        terms_sorted_by_df = []
        for key in sorted(df_terms.keys()):
            if type(df_terms[key]) == list:
                terms_sorted_by_df.extend(df_terms[key])
            else:
                terms_sorted_by_df.append(df_terms[key])

        term1 = terms_sorted_by_df[0]
        term2 = terms_sorted_by_df[1]

        df_term2, skip_pointer_term2, index_pointer_term2 = self.vocabulary[term2]
        posting_term1 = self.get_posting(term1)
        skips_term2 = self.importer.get_skip(skip_pointer_term2, df_term2)

        two_term_result = self.two_term_and_query(
                posting_term1, index_pointer_term2, skips_term2, df_term2
            )
        if len(terms_sorted_by_df) == 2:
            return two_term_result
        else:
            if two_term_result == []:
                return []
            
            term3 = terms_sorted_by_df[2]
            df_term3, skip_pointer_term3, index_pointer_term3 = self.vocabulary[term3]
            skips_term3 = self.importer.get_skip(skip_pointer_term3, df_term3)

            return self.two_term_and_query(
                two_term_result, index_pointer_term3, skips_term3, df_term3
            )

    def search_with_skips(self, searching_doc_id, skips_term2, start_index_pointer, df_term):
        # print("Searching doc_id {}".format(searching_doc_id))
        previous_pointer = start_index_pointer
        for doc_id, pointer_index in skips_term2:
            if doc_id == searching_doc_id:
                # print("Searching_doc_id was in skip list")
                return True
            if doc_id > searching_doc_id:
                # print("If it is, its in inverted index at pointer {} reading {}".format(previous_pointer, K_SKIPS))
                for doc_id in self.importer.get_posting_part(previous_pointer, K_SKIPS):
                    if doc_id == searching_doc_id:
                        return True
                    if doc_id > searching_doc_id:
                        return False
            previous_pointer = pointer_index

        # Si salio del for, es porque todos los doc ids son menores, si está, esta al final.
        #La primera posicion que lee, es el valor de la posting, por eso 1 +
        return searching_doc_id in self.importer.get_posting_part(previous_pointer, 1 + (df_term % K_SKIPS))

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