import struct
from constants import *
import json
from itertools import chain
from bitarray import bitarray

class Exporter:

    def __init__(self):
        self.pointers = {}
        self.pointers["gamma"] = {}
        self.pointers["variable"] = {}
        self.pointers["index"] = {}


    def metadata(self):
        metadata = {}
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

    def binario(self, doc_id):
        return bin(doc_id).replace("0b", "")

    def unario(self, doc_id):
        return "1"*(doc_id-1)+"0"

    def rmsb(self, bin_doc_id):
        return bin_doc_id[1:]

    def gamma_compress(self, doc_id):
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
        bits = ""
        while not finished:
            if len(bin_doc_id) <= 7:
                bits += "1" + bin_doc_id
                finished = True
            else:
                bits += "0" + bin_doc_id[0:7]
                bin_doc_id = bin_doc_id[7:]
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
            frequencies = []
            for posting in postings_lists:
                doc_id = posting[0]
                frequencies.append(posting[1])
                variable_compressed_doc_id = self.variable_compress(doc_id)
                variable_compressed_postings_lists += variable_compressed_doc_id

            compressed_posting = bitarray(variable_compressed_postings_lists)

            variable.write(compressed_posting)
            variable_pointer = variable_pointer_acumulator
            variable_pointer_acumulator += len(compressed_posting) // 8

            frequencies_string = ""
            for frequency in frequencies:
                frequencies_string += self.unario(frequency)
            rest = len(frequencies_string) % 8
            if rest != 0:
                padding = 8 - rest
                frequencies_string = frequencies_string + ("0" * padding)
            variable.write(bitarray(frequencies_string))
            variable_pointer_acumulator += len(frequencies_string) // 8

            self.pointers["variable"][term] = [variable_pointer, len(compressed_posting), len(frequencies_string)]

    def inverted_index_gamma(self, inverted_index):
        gamma = open(BIN_INVERTED_INDEX_GAMMA_FILEPATH, "wb")
        gamma_pointer_acumulator = 0

        for term in inverted_index:
            postings_lists = inverted_index[term]
            gamma_compressed_postings_lists = ""
            frequencies = []
            for posting in postings_lists:
                doc_id = posting[0]
                frequencies.append(posting[1])
                gamma_compressed_doc_id = self.gamma_compress(doc_id)
                gamma_compressed_postings_lists += gamma_compressed_doc_id

            len_before_padding = len(gamma_compressed_postings_lists)
            rest = len(gamma_compressed_postings_lists) % 8
            if rest != 0:
                padding = 8 - rest
                gamma_compressed_postings_lists = ("0" * padding) + gamma_compressed_postings_lists
            compressed_posting = bitarray(gamma_compressed_postings_lists)
            gamma.write(compressed_posting)
            gamma_pointer = gamma_pointer_acumulator
            gamma_pointer_acumulator += len(compressed_posting) // 8

            frequencies_string = ""
            for frequency in frequencies:
                frequencies_string += self.unario(frequency)
            rest = len(frequencies_string) % 8
            if rest != 0:
                padding = 8 - rest
                frequencies_string = frequencies_string + ("0" * padding)
            gamma.write(bitarray(frequencies_string))
            gamma_pointer_acumulator += len(frequencies_string) // 8

            self.pointers["gamma"][term] = [gamma_pointer, len_before_padding, len(frequencies_string)]


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
        string_format = "{}sIIIIIIII".format(self.terms_size)
        with open(BIN_VOCABULARY_FILEPATH, "wb") as f:
            for key in vocabulary:
                packed_data = struct.pack(
                    string_format, bytes(key, "utf-8"), vocabulary[key], self.pointers["index"][key], self.pointers["gamma"][key][0], self.pointers["gamma"][key][1], self.pointers["gamma"][key][2], self.pointers["variable"][key][0], self.pointers["variable"][key][1], self.pointers["variable"][key][2]
                )
                f.write(packed_data)

    def dgap_index(self, inverted_index):
        for posting_list in inverted_index.values():
            last_docid = 0
            for posting in posting_list:
                posting[0] = posting[0] - last_docid
                last_docid = posting[0]

        return inverted_index