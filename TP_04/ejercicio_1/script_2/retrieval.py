import struct
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
        self.normalizer = Normalizer(metadata["STEMMING_LANGUAGE"])
        self.entity_extractor = Entity_Extractor(metadata["STEMMING_LANGUAGE"])

    def get_posting(self, term):
        if self.metadata["EXTRACT_ENTITIES"]:
            rest, entities_list = self.entity_extractor.extract_entities(term)
            if len(entities_list) >= 1:
                #if rest != "":?
                #if len(entities_list) >= 2: ?
                #if entity != term? #Doesnt work for U.S.A > usa
                entity = entities_list[0]
                processed_term = entity
            else:
                processed_term = self.normalizer.normalize(term)
        else:
            processed_term = self.normalizer.normalize(term)

        with open(INDEX_FILES_PATH+BIN_INVERTED_INDEX_FILENAME, "rb") as f:
            try:
                df, pointer = self.vocabulary[processed_term]
            except:
                return []
            string_format = "{}I".format(df)

            f.seek(pointer*struct.calcsize("I"))
            content = f.read(struct.calcsize(string_format))
            unpacked_data = struct.unpack(string_format, content)
            
            return list(unpacked_data)

    def get_vocabulary(self):
        return self.vocabulary.keys()
