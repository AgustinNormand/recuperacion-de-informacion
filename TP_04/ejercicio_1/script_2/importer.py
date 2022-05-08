import struct
from constants import *
import json

class Importer:

    def __init__(self, terms_size, docnames_size):
        self.terms_size = terms_size
        self.docnames_size = docnames_size

    def read_vocabulary(self):
        with open(BIN_VOCABULARY_FILEPATH, "rb") as f:
            string_format = "{}s{}I{}I".format(self.terms_size, 1, 1)
            read_size = struct.calcsize(string_format)
            vocabulary = {}

            content = f.read(read_size)
            while content != b'':
                unpacked_data = struct.unpack(string_format, content) # leo bytes del 
                term, df, pointer = unpacked_data
                term = str(term, 'utf-8').rstrip('\x00')
                vocabulary[term] = (df, pointer)
                content = f.read(read_size)

        return vocabulary

    def read_docnames_ids_file(self):
        ids_docnames = {}
        with open(BIN_DOCNAMES_IDS_FILEPATH, "rb") as f:
            string_format = "{}s{}I".format(self.docnames_size, 1)
            read_size = struct.calcsize(string_format)
            content = f.read(read_size)

            while content != b'':
                unpacked_data = struct.unpack(string_format, content) # leo bytes del 
                docname, doc_id = unpacked_data
                #term = str(term, 'utf-8').rstrip('\x00')
                docname = str(docname, 'utf-8').rstrip('\x00')
                ids_docnames[doc_id] = docname
                content = f.read(read_size)
        return ids_docnames

    def read_inverted_index(self, vocabulary):
        inverted_index = {}
        with open(BIN_INVERTED_INDEX_FILEPATH, "rb") as f:
            for term in vocabulary:
                df, pointer = vocabulary[term]
                string_format = "{}I".format(df)
                f.seek(pointer*struct.calcsize("I"))
                content = f.read(struct.calcsize(string_format))
                unpacked_data = struct.unpack(string_format, content)
                inverted_index[term] = unpacked_data
        return inverted_index