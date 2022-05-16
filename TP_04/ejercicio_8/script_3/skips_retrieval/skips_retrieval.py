from skips_retrieval.importer import *
from constants import *

class Skips_Retrieval:
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

        return searching_doc_id in self.importer.get_posting_part(
            previous_pointer, 1 + (df_term % K_SKIPS)
        )

    def and_query(self, terms):
        term1, term2, term3 = self.get_terms_in_order(terms)

        df_term2, index_pointer_term2, skip_pointer_term2 = self.vocabulary[term2]
        posting_term1 = self.get_posting(term1)
        skips_term2 = self.importer.get_skips_part(skip_pointer_term2, df_term2)
        two_term_result = self.two_term_and_query_skips(
            posting_term1, index_pointer_term2, skips_term2, df_term2
        )
        if term3 == None:
            return two_term_result
        else:
            if two_term_result == []:
                return []

            df_term3, index_pointer_term3, skip_pointer_term3 = self.vocabulary[term3]
            skips_term3 = self.importer.get_skips_part(skip_pointer_term3, df_term3)

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
