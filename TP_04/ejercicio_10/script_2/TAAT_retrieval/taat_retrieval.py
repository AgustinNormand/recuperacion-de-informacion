from TAAT_retrieval.importer import *
from constants import *
import math

class TAAT_Retrieval:
    def __init__(self, metadata):
        self.metadata = metadata
        self.importer = Importer(metadata["TERMS_SIZE"])
        self.vocabulary = self.importer.read_vocabulary()

    def get_terms_in_order(self, terms):
        df_terms = {}
        for term in terms:
            df_term, _, _ = self.vocabulary[term]
            if df_term not in df_terms.keys():
                df_terms[df_term] = term
            else:
                if type(df_terms[df_term]) == list:
                    df_terms[df_term].append(term)
                else:
                    df_terms[df_term] = [df_terms[df_term], term]


        terms_sorted_by_df = []
        for key in sorted(df_terms.keys()):
            if type(df_terms[key]) == list:
                terms_sorted_by_df.extend(df_terms[key])
            else:
                terms_sorted_by_df.append(df_terms[key])
        return terms_sorted_by_df

    def search_with_skips(
            self, searching_doc_id, skips_term2, start_index_pointer, df_term
    ):
        previous_pointer = start_index_pointer
        for doc_id, pointer_index in skips_term2:
            if doc_id == searching_doc_id:
                return True
            if doc_id > searching_doc_id:
                for doc_id in self.importer.get_posting_part(previous_pointer, round(math.sqrt(df_term))):
                    if doc_id == searching_doc_id:
                        return True
                    if doc_id > searching_doc_id:
                        return False
            previous_pointer = pointer_index

        return searching_doc_id in self.importer.get_posting_part(
            previous_pointer, 1 + (df_term % round(math.sqrt(df_term)))
        )

    def and_query(self, terms):
        if len(terms) == 1:
            return self.get_posting(terms[0])

        terms_sorted_by_df = self.get_terms_in_order(terms)

        partial_result = self.get_posting(terms_sorted_by_df[0])
        terms_sorted_by_df.remove(terms_sorted_by_df[0])

        for term in terms_sorted_by_df:
            #print(terms_sorted_by_df)
            df_term, index_pointer_term, skip_pointer_term = self.vocabulary[term]
            skips_term = self.importer.get_skips_part(skip_pointer_term, df_term)
            partial_result = self.two_term_and_query_skips(
                partial_result, index_pointer_term, skips_term, df_term
            )
            if partial_result == []:
                break

        return partial_result

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


    def get_posting(self, term):
        try:
            df_term, index_pointer, skips_pointer = self.vocabulary[term]
            return self.importer.get_posting_part(index_pointer, df_term)
        except:
            return []

    def all_terms_in_vocabulary(self, terms):
        for term in terms:
            if term not in self.vocabulary.keys():
                return False
        return True

    def get_vocabulary(self):
        return self.vocabulary.keys()
