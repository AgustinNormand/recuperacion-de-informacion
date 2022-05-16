import struct
import matplotlib.pyplot as plt
import os
from constants import *
import json

class Exporter:
    def metadata(self):
        metadata = {}
        metadata["TERMS_SIZE"] = self.terms_size
        with open(INDEX_FILES_PATH+METADATA_FILE, 'w') as fp:
            json.dump(metadata, fp,  indent=4)

    def get_max_length(self, array):
        max_length = 0
        for value in array:
            if len(value) > max_length:
                max_length = len(value)
        return max_length

    def analize_terms_length(self, vocabulary):
            self.terms_size = self.get_max_length(vocabulary.keys())

    def inverted_index(self, inverted_index):
        self.inverted_index_pointers = {}
        self.skips_pointers = {}
        self.dgaps = {}

        inverted_index_string_format = "I"
        skips_string_format = "II"

        inverted_index_file = open(INDEX_FILES_PATH + BIN_INVERTED_INDEX_FILENAME, "wb")
        skips = open(INDEX_FILES_PATH + BIN_SKIPS_FILENAME, "wb")
        dgaps = open(INDEX_FILES_PATH + BIN_DGAPS_FILENAME, "wb")

        inverted_index_pointer_acumulator = 0
        skips_pointer_acumulator = 0
        dgaps_pointer_acumulator = 0

        for key in inverted_index:
            self.inverted_index_pointers[key] = inverted_index_pointer_acumulator
            self.skips_pointers[key] = skips_pointer_acumulator
            self.dgaps[key] = dgaps_pointer_acumulator

            doc_ids_writed = 0
            posting = inverted_index[key]
            last_docid = 0
            for doc_id in posting:
                packed_data = struct.pack(inverted_index_string_format, doc_id)
                inverted_index_file.write(packed_data)
                doc_ids_writed += 1

                # This is for dgaps
                packed_data = struct.pack(inverted_index_string_format, doc_id - last_docid)
                dgaps.write(packed_data)
                dgaps_pointer_acumulator += struct.calcsize(inverted_index_string_format)
                last_docid = doc_id
                #

                if doc_ids_writed == K_SKIPS:
                    packed_data = struct.pack(skips_string_format, doc_id, inverted_index_pointer_acumulator)
                    skips.write(packed_data)
                    doc_ids_writed = 0
                    skips_pointer_acumulator += struct.calcsize(skips_string_format)
                inverted_index_pointer_acumulator += struct.calcsize(inverted_index_string_format)



    def vocabulary_file(self, vocabulary):
        self.analize_terms_length(vocabulary)
        string_format = "{}sIIII".format(self.terms_size)
        with open(INDEX_FILES_PATH + BIN_VOCABULARY_FILENAME, "wb") as f:
            for key in vocabulary:
                packed_data = struct.pack(
                    string_format, bytes(key, "utf-8"), vocabulary[key], self.inverted_index_pointers[key], self.skips_pointers[key], self.dgaps[key]
                )
                f.write(packed_data)
