from importer import Importer
from constants import *
import sys
sys.path.append('../script_1')
from normalizer import *
from entity_extractor import *

class Retrieval():
    def __init__(self, metadata):
        self.metadata = metadata
        self.importer = Importer(metadata["TERMS_SIZE"], metadata["DOCNAMES_SIZE"])
        self.vocabulary = self.importer.read_vocabulary()
        #print(self.vocabulary)
        self.importer.read_inverted_index(self.vocabulary)
        self.normalizer = Normalizer(metadata["STEMMING_LANGUAGE"])
        self.entity_extractor = Entity_Extractor(metadata["STEMMING_LANGUAGE"])

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
        return self.vocabulary.keys()
