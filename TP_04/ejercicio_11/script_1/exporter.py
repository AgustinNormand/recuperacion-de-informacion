import struct
from constants import *
import json
from itertools import chain
#import binascii
import math

import matplotlib.pyplot as plt
import os
import time
from bitarray import bitarray

class Exporter:

    def __init__(self):
        self.pointers = {}
        self.pointers["gamma"] = {}
        self.pointers["variable"] = {}
        self.pointers["index"] = {}


    def metadata(self):
        metadata = {}
#        metadata["DOCNAMES_SIZE"] = self.docnames_size
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

#    def analize_document_titles_length(self, docnames_ids):
#        if STRING_STORE_CRITERION == "MAX":
#            self.docnames_size = self.get_max_length(docnames_ids.keys())
#        else:
#            self.docnames_size = DOCNAMES_SIZE


#    def save_docnames_ids_file(self, docnames_ids):
#        self.docnames_ids = docnames_ids
#        self.analize_document_titles_length(docnames_ids)
#        docnames_ids_list = [(bytes(k, "utf-8"), v) for k, v in docnames_ids.items()]
#        string_format = "{}s{}I".format(self.docnames_size, 1)
#        with open(BIN_DOCNAMES_IDS_FILEPATH, "wb") as f:
#            for value in docnames_ids_list:
#                packed_data = struct.pack(string_format, *value)
#                f.write(packed_data)
        # Mejorar y no hacer escrituras repetidas, sino una sola escritura.
        # Mejorar, no usar el path absoluto. Incluso, no usar docNN.txt, solo almacenar el NN

    def binario(self, doc_id):
        return bin(doc_id).replace("0b", "")

    def unario(self, doc_id):
        return "1"*(doc_id-1)+"0"

    def rmsb(self, bin_doc_id):
        return bin_doc_id[1:]

    def gamma_compress(self, doc_id):
        #print("Docid: {}, en binario: {}, longitud: {}, unario de longitud: {}, rmsb: {}".format(doc_id, self.binario(doc_id), len(self.binario(doc_id)), self.unario(len(self.binario(doc_id))), self.rmsb(self.binario(doc_id))))
        binario = self.binario(doc_id)
        len_bin = len(self.binario(doc_id))
        u = self.unario(len_bin)
        rmsb = self.rmsb(binario)
        return u+rmsb

    def variable_length(self, bin_doc_id):
        rest = len(bin_doc_id) % 7
        if rest != 0:
            padding = 7 - rest
            bin_doc_id = ("0" * padding) + bin_doc_id
        finished = False
        #bytes = []
        bits = ""
        while not finished:
            if len(bin_doc_id) <= 7:
                #bytes.append("1" + bin_doc_id)
                bits += "1" + bin_doc_id
                finished = True
            else:
                #bytes.append("0" + bin_doc_id[0:7])
                bits += "0" + bin_doc_id[0:7]
                bin_doc_id = bin_doc_id[7:]
        #return bytes
        return bits

    def variable_compress(self, doc_id):
        binario = self.binario(doc_id)
        return self.variable_length(binario)

    def inverted_index_variable(self, inverted_index):
        variable = open(BIN_INVERTED_INDEX_VARIABLE_FILEPATH, "wb")
        variable_pointer_acumulator = 0
        for term in inverted_index:
            postings_lists = inverted_index[term]
            variable_compressed_postings_lists = ""
            for posting in postings_lists:
                doc_id = posting[0]
                frecuencia = posting[1] #TODO
                variable_compressed_doc_id = self.variable_compress(doc_id)
                variable_compressed_postings_lists += variable_compressed_doc_id

            compressed_posting = bitarray(variable_compressed_postings_lists)

            variable.write(compressed_posting)
            self.pointers["variable"][term] = [variable_pointer_acumulator, len(compressed_posting)]
            variable_pointer_acumulator += len(compressed_posting) // 8
        #print(self.pointers["variable"])

    def inverted_index_gamma(self, inverted_index):
        gamma = open(BIN_INVERTED_INDEX_GAMMA_FILEPATH, "wb")
        gamma_pointer_acumulator = 0

        for term in inverted_index:
            postings_lists = inverted_index[term]
            gamma_compressed_postings_lists = ""
            for posting in postings_lists:

                doc_id = posting[0]
                frecuencia = posting[1] #TODO
                gamma_compressed_doc_id = self.gamma_compress(doc_id)
                gamma_compressed_postings_lists += gamma_compressed_doc_id
                if term == "1st":
                    print(doc_id)
                    print(self.gamma_compress(doc_id))
                    print(gamma_compressed_postings_lists)


            len_before_padding = len(gamma_compressed_postings_lists)
            rest = len(gamma_compressed_postings_lists) % 8
            if rest != 0:
                padding = 8 - rest
                gamma_compressed_postings_lists = ("0" * padding) + gamma_compressed_postings_lists
            #if term == "german":
                #print(postings_lists)
                #print(gamma_compressed_postings_lists)
                #print(len(gamma_compressed_postings_lists))
                #print(gamma.tell())
            compressed_posting = bitarray(gamma_compressed_postings_lists)
            #print(len(compressed_posting))
            gamma.write(compressed_posting)
            self.pointers["gamma"][term] = [gamma_pointer_acumulator, len_before_padding]
            gamma_pointer_acumulator += len(compressed_posting) // 8
        #print(self.pointers["gamma"])

    def inverted_index(self, inverted_index):
        entry_string_format = "IHxx"
        with open(BIN_INVERTED_INDEX_FILEPATH, "wb") as f:
            index_pointer_acumulator = 0
            for term in inverted_index:
                postings_lists = inverted_index[term]
                complete_string_format = entry_string_format*(len(postings_lists))
                packed_data = struct.pack(complete_string_format, *list(chain(*postings_lists)))
                f.write(packed_data)
                self.pointers["index"][term] = index_pointer_acumulator
                index_pointer_acumulator += struct.calcsize(complete_string_format)

    def analize_terms_length(self, vocabulary):
        self.vocabulary = vocabulary
        if STRING_STORE_CRITERION == "MAX":
            self.terms_size = self.get_max_length(vocabulary.keys())
        else:
            self.terms_size = TERMS_SIZE

    def vocabulary_file(self, vocabulary):
        self.analize_terms_length(vocabulary)
        string_format = "{}sIIIIII".format(self.terms_size)
        with open(BIN_VOCABULARY_FILEPATH, "wb") as f:
            for key in vocabulary:
                #print(self.pointers["gamma"][key][0], self.pointers["gamma"][key][1], self.pointers["variable"][key][0], self.pointers["variable"][key][1])
                packed_data = struct.pack(
                    string_format, bytes(key, "utf-8"), vocabulary[key], self.pointers["index"][key], self.pointers["gamma"][key][0], self.pointers["gamma"][key][1], self.pointers["variable"][key][0], self.pointers["variable"][key][1]
                )
                f.write(packed_data)
