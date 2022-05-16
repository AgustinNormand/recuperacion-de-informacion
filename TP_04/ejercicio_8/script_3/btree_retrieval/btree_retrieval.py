from btree_retrieval.importer import *


class Btree_Retrieval:
    def __init__(self, metadata):
        self.metadata = metadata
        self.importer = Importer(metadata["TERMS_SIZE"])
        self.vocabulary = self.importer.read_vocabulary()
        self.inverted_index = self.importer.read_inverted_index_btree(self.vocabulary)

    def all_terms_in_vocabulary(self, terms):
        for term in terms:
            if term not in self.vocabulary.keys():
                return False
        return True

    def get_terms_in_order(self, terms):
        df_terms = {}
        for term in terms:
            df_term, _ = self.vocabulary[term]
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

    def two_term_and_query(
        self, keys_term1, tree_term2
    ):
        result = []
        for doc_id in keys_term1:
            if tree_term2.has_key(doc_id):
                result.append(doc_id)
        return result

    def and_query(self, terms):
        if not self.all_terms_in_vocabulary(terms):
            return []

        term1, term2, term3 = self.get_terms_in_order(terms)

        two_term_result = self.two_term_and_query(list(self.inverted_index[term1].keys()), self.inverted_index[term2])
        if term3 == None:
            return two_term_result
        else:
            if two_term_result == []:
                return []
            return self.two_term_and_query(two_term_result, self.inverted_index[term3])

    def get_vocabulary(self):
        return self.vocabulary
