import re
import struct

import sys
sys.path.append('../ejercicio_1/script_2')
sys.path.append('../ejercicio_1/script_1')

from importer import *
from normalizer import *
from entity_extractor import *
#from constants import *

class Retrieval():
    def __init__(self, metadata, on_memory = False):
        self.metadata = metadata
        self.importer = Importer(metadata["TERMS_SIZE"], metadata["DOCNAMES_SIZE"])
        self.vocabulary = self.importer.read_vocabulary()
        self.ids_docnames = self.importer.read_docnames_ids_file()
        self.normalizer = Normalizer(metadata["STEMMING_LANGUAGE"])
        self.entity_extractor = Entity_Extractor(metadata["STEMMING_LANGUAGE"])
        self.on_memory = on_memory
        if self.on_memory:
            self.inverted_index = self.importer.read_inverted_index(self.vocabulary)

    def and_query(self, term1, term2, term3=None):
        posting1 = self.get_posting(term1)
        posting2 = self.get_posting(term2)
        if term3 == None:
            return set(posting1).intersection(set(posting2))
        else:
            posting3 = self.get_posting(term3)
            return set(posting1).intersection(set(posting2)).intersection(set(posting3))

    def or_query(self, term1, term2):
        posting1 = self.get_posting(term1)
        posting2 = self.get_posting(term2)
        return set(posting1).union(set(posting2))

    def not_query(self, term1, term2):
        posting1 = self.get_posting(term1)
        posting2 = self.get_posting(term2)
        return set(posting1).difference(set(posting2))

    def one_term_query(self, user_input):
        try:
            term1, term2 = user_input.split(AND_SYMBOL)
            return self.and_query(term1, term2)
        except Exception as e:
            pass

        try:
            term1, term2 = user_input.split(OR_SYMBOL)
            return self.or_query(term1, term2)
        except Exception as e:
            pass
    
        try:
            term1, term2 = user_input.split(NOT_SYMBOL)
            return self.not_query(term1, term2)
        except Exception as e:
            pass

    def two_term_query(self, user_input):
        try:
            term1, term2, term3 = user_input.split(AND_SYMBOL)
            return self.and_query(term1, term2, term3)
        except Exception as e:
            pass

        try:
            parenthesis = re.findall(r'\((.*?)\)', user_input)[0]
            parenthesis_resultset = set(self.query(parenthesis))
            rest = user_input.replace("("+parenthesis+")", "")
            if AND_SYMBOL in rest:
                term = rest.replace(AND_SYMBOL, "")
                return set(self.get_posting(term)).intersection(parenthesis_resultset)
            if NOT_SYMBOL in rest:
                term = rest.replace(NOT_SYMBOL, "")
                return parenthesis_resultset.difference(set(self.get_posting(term)))
            if OR_SYMBOL in rest:
                term = rest.replace(OR_SYMBOL, "")
                return parenthesis_resultset.union(set(self.get_posting(term)))
        except Exception as e:
            #print(e)
            pass
    


    def query(self, user_input):
        ands = user_input.count(AND_SYMBOL)
        ors = user_input.count(OR_SYMBOL)
        nots = user_input.count(NOT_SYMBOL) 
        #if (ands+ors+nots) == 0?
        try:
            if (ands+ors+nots) == 1:
                return sorted(list(self.one_term_query(user_input)))
            else:
                if (ands+ors+nots) > 1:
                    return sorted(list(self.two_term_query(user_input)))
                else:
                    return sorted(list(self.get_posting(user_input)))
        except:
            return []

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

        if self.on_memory:
            try:
                return self.inverted_index[processed_term]
            except:
                return {}
        else:
            with open(BIN_INVERTED_INDEX_FILEPATH, "rb") as f:
                try:
                    df, pointer = self.vocabulary[processed_term]
                except:
                    return {}
                string_format = "{}I".format(df)

                f.seek(pointer*struct.calcsize("I"))
                content = f.read(struct.calcsize(string_format))
                unpacked_data = struct.unpack(string_format, content)
                
                return unpacked_data

    def get_vocabulary(self):
        return self.vocabulary.keys()




    # (casa-perro)&gato
    # gato&(casa-perro)
    # casa&perro&freud

    # casa-perro 

    #(casa-perro)&ministro
    #[4, 47, 48, 70, 102, 173, 422]

    #(ministro&casa)-perro
    #[]


    #casa&perro
    #[128]

    #perro&casa
    #[128]

    #casa|perro
    #[4, 8, 20, 24, 29, 43, 47, 48, 50, 55, 66, 70, 73, 84, 88, 92, 95, 100, 102, 104, 110, 115, 116, 123, 126, 128, 135, 140, 152, 161, 171, 173, 180, 195, 198, 200, 221, 222, 232, 239, 240, 241, 249, 250, 264, 265, 267, 268, 279, 304, 307, 315, 317, 318, 319, 320, 324, 326, 341, 349, 353, 355, 359, 374, 386, 399, 408, 411, 420, 422, 433, 438, 439, 453, 456, 463, 468, 482, 486, 488, 492]
    #(está el 128)

    #casa-perro
    #[4, 8, 20, 24, 29, 43, 47, 48, 50, 55, 66, 70, 73, 84, 88, 92, 95, 100, 102, 104, 110, 115, 116, 123, 126, 135, 140, 152, 161, 171, 173, 180, 195, 198, 200, 221, 222, 232, 239, 240, 241, 249, 250, 264, 265, 267, 268, 279, 304, 307, 315, 317, 318, 319, 320, 324, 326, 341, 349, 353, 355, 359, 374, 386, 399, 408, 411, 420, 422, 433, 438, 439, 453, 456, 463, 468, 482, 486, 488, 492]
    #(no esta el 128)