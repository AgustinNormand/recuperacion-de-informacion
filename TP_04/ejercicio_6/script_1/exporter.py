import struct
from constants import *
import json
from itertools import chain
import binascii
import math

import matplotlib.pyplot as plt
import os

class Exporter:
    def metadata(self):
        metadata = {}
        metadata["DOCNAMES_SIZE"] = self.docnames_size
        metadata["TERMS_SIZE"] = self.terms_size
        metadata["STEMMING_LANGUAGE"] = STEMMING_LANGUAGE
        metadata["EXTRACT_ENTITIES"] = EXTRACT_ENTITIES
        with open(METADATA_FILE, 'w') as fp:
            json.dump(metadata, fp,  indent=4)

    def get_max_length(self, array):
        max_length = 0
        for value in array:
            if len(value) > max_length:
                max_length = len(value)
        return max_length

    def analize_document_titles_length(self, docnames_ids):
        if STRING_STORE_CRITERION == "MAX":
            self.docnames_size = self.get_max_length(docnames_ids.keys())
        else:
            self.docnames_size = DOCNAMES_SIZE

    def save_docnames_ids_file(self, docnames_ids):
        self.docnames_ids = docnames_ids
        self.analize_document_titles_length(docnames_ids)
        docnames_ids_list = [(bytes(k, "utf-8"), v) for k, v in docnames_ids.items()]
        string_format = "{}s{}I".format(self.docnames_size, 1)
        with open(BIN_DOCNAMES_IDS_FILEPATH, "wb") as f:
            for value in docnames_ids_list:
                packed_data = struct.pack(string_format, *value)
                f.write(packed_data)
    
    def save_positions(self, inverted_index):
        string_format = "I"
        pointer_acumulator = 0
        with open(BIN_POSITIONS_FILEPATH, "wb") as f:
            for term in inverted_index:
                for posting_list in inverted_index[term]:
                    _, frequency, positions = posting_list
                    complete_string_format = string_format*len(positions)
                    f.write(struct.pack(complete_string_format, *positions))
                    posting_list[2] = pointer_acumulator
                    pointer_acumulator += struct.calcsize(complete_string_format)
                    
                    if len(positions) != frequency:
                        print("len(positions) != frequency")


    def inverted_index(self, inverted_index, vocabulary):
        entry_string_format = "IHIxxxx"
        pointer_acumulator = 0
        with open(BIN_INVERTED_INDEX_FILEPATH, "wb") as f:
            for term in inverted_index:
                postings_lists = inverted_index[term]
                complete_string_format = entry_string_format*(len(postings_lists))
                packed_data = struct.pack(complete_string_format, *list(chain(*postings_lists)))
                f.write(packed_data)
                vocabulary[term] = [vocabulary[term], pointer_acumulator]
                pointer_acumulator += struct.calcsize(complete_string_format)

    def analize_terms_length(self, vocabulary):
        self.vocabulary = vocabulary
        if STRING_STORE_CRITERION == "MAX":
            self.terms_size = self.get_max_length(vocabulary.keys())
        else:
            self.terms_size = TERMS_SIZE

    def vocabulary_file(self, vocabulary):
        self.analize_terms_length(vocabulary)
        string_format = "{}s{}I{}I".format(self.terms_size, 1, 1)
        with open(BIN_VOCABULARY_FILEPATH, "wb") as f:
            for key in vocabulary:
                df, pointer = vocabulary[key]
                packed_data = struct.pack(
                    string_format, bytes(key, "utf-8"), df, pointer
                )
                f.write(packed_data)

    ## OVERHEAD AND STATISTICS
    def export_all_statistics(self):
        self.collection_overhead()

    def get_size(self, directory):
        size = 0
        for path, dirs, files in os.walk(directory):
            for f in files:
                fp = os.path.join(path, f)
                size += os.path.getsize(fp)
        return size

    def collection_overhead(self):
        corpus_size = self.get_size(DIRPATH)
        index_size = self.get_size(INDEX_FILES_PATH)

        print("\r")
        print(
            "Corpus Size: {} bytes, Index Size: {} bytes".format(
                corpus_size, index_size
            )
        )
        print("Overhead: {}".format(index_size / (corpus_size + index_size)))