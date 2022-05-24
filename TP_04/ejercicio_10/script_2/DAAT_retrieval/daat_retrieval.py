from DAAT_retrieval.importer import *
from constants import *

class DAAT_Retrieval:
    def __init__(self, metadata):
        self.metadata = metadata
        self.importer = Importer(metadata["TERMS_SIZE"])
        self.vocabulary = self.importer.read_vocabulary()

    def get_posting(self, term):
        try:
            df_term, index_pointer, skips_pointer = self.vocabulary[term]
            return self.importer.get_posting_part(index_pointer, df_term)
        except:
            return []

    def create_posting_dictionary(self, terms):
        postings = {}
        for term in terms:
            postings[term] = {}
            postings[term]["postings"] = list(self.get_posting(term))
            postings[term]["pointer"] = 0
        return postings

    def get_actual(self, posting_dictionary, term):
        pointer = posting_dictionary[term]["pointer"]
        posting = posting_dictionary[term]["postings"]

        if pointer == len(posting):
            return None
        else:
            return posting[pointer]

    def next(self, posting_dictionary, term):
        posting_dictionary[term]["pointer"] += 1

    def get_term_of_min_docid(self, posting_dictionary):
        min_docid = None
        term_min = None

        for term in posting_dictionary:
            doc_id = self.get_actual(posting_dictionary, term)
            if min_docid == None or doc_id < min_docid:
                min_docid = doc_id
                term_min = term
        return term_min

    def same_docid(self, posting_dictionary):
        last_docid = None
        for term in posting_dictionary:
            doc_id = self.get_actual(posting_dictionary, term)
            if last_docid == None:
                last_docid = doc_id
            else:
                if last_docid != doc_id:
                    return False
        return True

    def any_none(self, posting_dictionary):
        for term in posting_dictionary:
            doc_id = self.get_actual(posting_dictionary, term)
            if doc_id == None:
                return True
        return False

    def get_any_docid(self, posting_dictionary):
        for term in posting_dictionary:
            return self.get_actual(posting_dictionary, term)

    def and_query(self, terms):
        result = []

        if len(terms) == 1:
            return self.get_posting(terms[0])

        posting_dictionary = self.create_posting_dictionary(terms)

        return self.and_query_not_modular(posting_dictionary)


#        while not self.any_none(posting_dictionary):
#            if self.same_docid(posting_dictionary):
#                result.append(self.get_any_docid(posting_dictionary))
#                for term in terms:
#                    self.next(posting_dictionary, term)
#            else:
#                self.next(posting_dictionary, self.get_term_of_min_docid(posting_dictionary))
#
#        return result

    def and_query_not_modular(self, posting_dictionary):
        result = []
        while True:
            last_docid = None
            same_docid = True
            min_docid = None
            term_min = None
            for term in posting_dictionary:
                doc_id = self.get_actual(posting_dictionary, term)
                if doc_id == None:
                    return result

                if min_docid == None:
                    min_docid = doc_id
                    term_min = term
                else:
                    if doc_id < min_docid:
                        min_docid = doc_id
                        term_min = term

                if last_docid == None:
                    last_docid = doc_id
                else:
                    if doc_id != last_docid:
                        same_docid = False

            if same_docid:
                result.append(last_docid)
                for term in posting_dictionary:
                    posting_dictionary[term]["pointer"] += 1
            else:
                posting_dictionary[term_min]["pointer"] += 1

    def get_vocabulary(self):
        return self.vocabulary.keys()

    def all_terms_in_vocabulary(self, terms):
        for term in terms:
            if term not in self.vocabulary.keys():
                return False
        return True

