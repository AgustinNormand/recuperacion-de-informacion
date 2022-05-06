import struct

import sys
sys.path.append('../script_1')
from constants import *

class Importer:

    def read_vocabulary(self):
        with open(INDEX_FILES_PATH+BIN_VOCABULARY_FILENAME, "rb") as f:
            string_format = "{}s{}I{}I".format(TERMS_SIZE, 1, 1)
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
        with open(INDEX_FILES_PATH+BIN_DOCNAMES_IDS_FILENAME, "rb") as f:
            string_format = "{}s{}I".format(DOCNAMES_SIZE, 1)
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