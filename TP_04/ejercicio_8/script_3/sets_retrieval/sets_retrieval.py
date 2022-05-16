import re
import struct


from sets_retrieval.importer import *
#from constants import *

class Sets_Retrieval():
    def __init__(self, metadata):
        self.metadata = metadata
        self.importer = Importer(metadata["TERMS_SIZE"])
        self.vocabulary = self.importer.read_vocabulary()
        self.inverted_index = self.importer.read_inverted_index(self.vocabulary)

    def and_query(self, terms):
        if len(terms) == 2:
            return sorted(list(set(self.inverted_index[terms[0]]).intersection(self.inverted_index[terms[1]])))
