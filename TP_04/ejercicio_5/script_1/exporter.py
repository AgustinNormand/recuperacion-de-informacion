import struct
from constants import *
import json
from itertools import chain
import binascii

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
        self.analize_document_titles_length(docnames_ids)
        docnames_ids_list = [(bytes(k, "utf-8"), v) for k, v in docnames_ids.items()]
        string_format = "{}s{}I".format(self.docnames_size, 1)
        with open(BIN_DOCNAMES_IDS_FILEPATH, "wb") as f:
            for value in docnames_ids_list:
                packed_data = struct.pack(string_format, *value)
                f.write(packed_data)
        # Mejorar y no hacer escrituras repetidas, sino una sola escritura.
        # Mejorar, no usar el path absoluto. Incluso, no usar docNN.txt, solo almacenar el NN

    def inverted_index(self, inverted_index):
        entry_string_format = "IHxx"
        with open(BIN_INVERTED_INDEX_FILEPATH, "wb") as f:
            for term in inverted_index:
                postings_lists = inverted_index[term]
                complete_string_format = entry_string_format*(len(postings_lists))
                packed_data = struct.pack(complete_string_format, *list(chain(*postings_lists)))
                f.write(packed_data)

    def analize_terms_length(self, vocabulary):
        if STRING_STORE_CRITERION == "MAX":
            self.terms_size = self.get_max_length(vocabulary.keys())
        else:
            self.terms_size = TERMS_SIZE

    def vocabulary_file(self, vocabulary):
        self.analize_terms_length(vocabulary)
        string_format = "{}s{}I{}I".format(self.terms_size, 1, 1)
        last_df = 0
        with open(BIN_VOCABULARY_FILEPATH, "wb") as f:
            for key in vocabulary:
                packed_data = struct.pack(
                    string_format, bytes(key, "utf-8"), vocabulary[key], last_df 
                )
                f.write(packed_data)
                last_df += vocabulary[key]