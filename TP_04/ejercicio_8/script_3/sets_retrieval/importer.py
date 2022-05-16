import struct
from constants import *

class Importer:
    def __init__(self, terms_size):
        self.terms_size = terms_size

    def read_vocabulary(self):
        with open(INDEX_FILES_PATH + BIN_VOCABULARY_FILENAME, "rb") as f:
            string_format = "{}sIIII".format(self.terms_size)
            read_size = struct.calcsize(string_format)
            vocabulary = {}

            content = f.read(read_size)
            while content != b'':
                unpacked_data = struct.unpack(string_format, content) # leo bytes del 
                term, df, pointer_index, pointer_skips, pointer_dgaps = unpacked_data
                term = str(term, 'utf-8').rstrip('\x00')
                vocabulary[term] = (df, pointer_index)
                content = f.read(read_size)

        return vocabulary

    def get_posting_part(self, pointer, amount):
        with open(INDEX_FILES_PATH + BIN_INVERTED_INDEX_FILENAME, "rb") as f:
            f.seek(pointer)
            string_format = "{}I".format(amount)
            content = f.read(struct.calcsize(string_format))
            unpacked_data = struct.unpack(string_format, content)
            return unpacked_data

    def get_skips_part(self, pointer, df):
        with open(INDEX_FILES_PATH + BIN_SKIPS_FILENAME, "rb") as f:
            string_format = "II" * (df // K_SKIPS)
            f.seek(pointer)
            content = f.read(struct.calcsize(string_format))
            unpacked_data = struct.unpack(string_format, content)

            skips = []
            i = 0
            while i < len(unpacked_data):
                doc_id = unpacked_data[i]
                pointer = unpacked_data[i + 1]
                skips.append([doc_id, pointer])
                i += 2
            return skips

    def read_inverted_index(self, vocabulary):
        inverted_index = {}
        for term in vocabulary:
            df, pointer_index = vocabulary[term]
            inverted_index[term] = self.get_posting_part(pointer_index, df)
        return inverted_index
