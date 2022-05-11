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
        self.documents_norm = self.importer.read_documents_norm(self.docnames_ids)
        #print(self.documents_norm)

    ## Query processor

    def obtain_normalized_terms(self, user_input):
        terms = user_input.split(" ")
        normalizedTerms_frequency = {}
        for term in terms:
            normalized_term = self.normalizer.normalize(term)
            if normalized_term in self.vocabulary.keys():
                if normalized_term in normalizedTerms_frequency.keys():
                    normalizedTerms_frequency[normalized_term] += 1
                else:
                    normalizedTerms_frequency[normalized_term] = 1
            # else:
            # print("{} removed from query, not in vocabulary".format(term))
        return normalizedTerms_frequency

    def obtain_query_vector(self, normalizedTerms_frequency, terms_idf, max_frequency):
        query_vector = {}
        for term in normalizedTerms_frequency:
            term_frequency = normalizedTerms_frequency[term]
            term_idf = terms_idf[term]
            query_vector[term] = (0.5 + 0.5 * term_frequency / max_frequency) * term_idf
        return query_vector

    def obtain_idf(self, normalizedTerms_frequency):
        collection_size = len(self.docnames_ids)
        terms_idf = {}
        for term in normalizedTerms_frequency:
            df, _ = self.vocabulary[term]
            terms_idf[term] = math.log(collection_size / df)
        return terms_idf

    def get_max_frequency(self, normalizedTerms_frequency):
        return max(normalizedTerms_frequency.values())

    def get_query_norm(self, query_vector):
        acum = 0
        for term in query_vector:
            acum += math.pow(query_vector[term], 2)
        return math.sqrt(acum)

    ##

    ## Documents processor

    def get_documents_scores(self, normalized_terms, terms_idf, query_vector):
        docid_partialScore = {}
        for normalized_term in normalized_terms:
            for doc_id, tf in self.importer.read_posting(
                normalized_term, self.vocabulary
            ):
                document_term_weight = tf * terms_idf[normalized_term]
                if doc_id in docid_partialScore.keys():
                    docid_partialScore[doc_id] += (
                        document_term_weight * query_vector[normalized_term]
                    )
                    
                else:
                    docid_partialScore[doc_id] = (
                        document_term_weight * query_vector[normalized_term]
                    )
        return docid_partialScore

    def compute_scores(self, docids_partialScores, query_norm):
        docids_finalScore = {}
        for doc_id in docids_partialScores:
            if query_norm == 0 or self.documents_norm[doc_id] == 0:
                pass
            else:
                score = docids_partialScores[doc_id]/(query_norm*self.documents_norm[doc_id])
                if score != 0:
                    docids_finalScore[doc_id] = score
        return docids_finalScore
    ##

    ## Entities
    def obtain_normalized_terms_with_entities(self, user_input):
        normalizedTerms_frequency = {}
        rest, entities_list = self.entity_extractor.extract_entities(user_input)
        for entity in entities_list:
            if entity in normalizedTerms_frequency.keys():
                normalizedTerms_frequency[entity] += 1
            else:
                normalizedTerms_frequency[entity] = 1

        terms = rest.split(" ")
        for term in terms:
            normalized_term = self.normalizer.normalize(term)
            if normalized_term in self.vocabulary.keys():
                if normalized_term in normalizedTerms_frequency.keys():
                    normalizedTerms_frequency[normalized_term] += 1
                else:
                    normalizedTerms_frequency[normalized_term] = 1
            # else:
            # print("{} removed from query, not in vocabulary".format(term))
        return normalizedTerms_frequency
    ##

    def query(self, user_input):
        if self.metadata["EXTRACT_ENTITIES"]:
            normalizedTerms_frequency = self.obtain_normalized_terms_with_entities(user_input)
        else:
            normalizedTerms_frequency = self.obtain_normalized_terms(user_input)
        terms_idf = self.obtain_idf(normalizedTerms_frequency)
        max_frequency = self.get_max_frequency(normalizedTerms_frequency)
        query_vector = self.obtain_query_vector(
                normalizedTerms_frequency, terms_idf, max_frequency
            )
        query_norm = self.get_query_norm(query_vector)

        docids_partialScores = self.get_documents_scores(
                normalizedTerms_frequency.keys(), terms_idf, query_vector
            )

        scores = self.compute_scores(docids_partialScores, query_norm)

        sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

        return sorted_scores
            
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
