import struct
from constants import *
from bitstring import BitArray

class Importer:

    def __init__(self, terms_size):
        self.terms_size = terms_size

    def read_vocabulary(self):
        with open(BIN_VOCABULARY_FILEPATH, "rb") as f:
            string_format = "{}s8I".format(self.terms_size)
            read_size = struct.calcsize(string_format)
            vocabulary = {}

            content = f.read(read_size)
            while content != b'':
                unpacked_data = struct.unpack(string_format, content)
                term, df, index_pointer, gamma_pointer, gamma_bits, gamma_frequencies_len, variable_pointer, variable_bits, variable_frequencies_len = unpacked_data
                term = str(term, 'utf-8').rstrip('\x00')
                vocabulary[term] = (df, index_pointer, gamma_pointer, gamma_bits, gamma_frequencies_len, variable_pointer, variable_bits, variable_frequencies_len)
                content = f.read(read_size)

        return vocabulary

    def decompress_variable(self, data):
        bin_data = BitArray(data)
        binary = bin_data.bin
        doc_ids = []
        bin_acumulator = ""
        while binary != '':
            end_of_number = int(binary[0]) == 1
            bin_acumulator += binary[1:8]
            binary = binary[8:]
            if end_of_number:
                doc_ids.append(int(bin_acumulator, 2))
                bin_acumulator = ""
        return doc_ids

    def decompress_frequencies(self, data, amount):
        bin_data = BitArray(data)
        binary = bin_data.bin

        frequencies = []

        while binary != "" and len(frequencies) < amount: #Por el padding
            if int(binary[0]) == 0:
                binary = binary[1:]
                unary_part = "0"
            else:
                i = 0
                unary_part = ""
                while int(binary[i]) != 0:
                    unary_part += binary[i]
                    i += 1
                binary = binary[i + 1:]
                unary_part += "0"
            frequencies.append(self.decompress_unary(unary_part, False))
        return frequencies

    def read_posting_variable(self, term, vocabulary, dgaps=False):

        with open(BIN_INVERTED_INDEX_VARIABLE_FILEPATH, "rb") as f:
            try:
                df, index_pointer, gamma_pointer, gamma_bits, gamma_frequencies_len, variable_pointer, variable_bits, variable_frequencies_len = vocabulary[term]
            except:
                return []
            f.seek(variable_pointer)
            data = f.read(variable_bits // 8)
            doc_ids = self.decompress_variable(data)
            frequencies = f.read(variable_frequencies_len // 8)
            frequencies = self.decompress_frequencies(frequencies, len(doc_ids))

            postings_lists = []
            last_doc_id = 0
            for i in range(len(doc_ids)):
                if dgaps:
                    postings_lists.append([doc_ids[i]+last_doc_id, frequencies[i]])
                    last_doc_id = doc_ids[i]
                else:
                    postings_lists.append([doc_ids[i], frequencies[i]])

            return postings_lists

    def decompress_unary(self, data, zero=True):
        if zero:
            acum = 0
        else:
            acum = 1
        for i in data:
            if int(i) == 1:
                acum += 1
            else:
                return acum

    def decompress_gamma(self, data, padding):
        doc_ids = []
        bin_data = BitArray(data)
        binary = bin_data.bin

        binary = binary[padding:]

        while binary != "":
            if int(binary[0]) == 0:
                binary = binary[1:]
                unary_part = "0"
            else:
                i = 0
                unary_part = ""
                while int(binary[i]) != 0:
                    unary_part += binary[i]
                    i += 1
                binary = binary[i+1:]
                unary_part += "0"
            bits_to_read = self.decompress_unary(unary_part)
            rmsb = "1"
            for i in range(bits_to_read):
                rmsb += binary[i]
            doc_ids.append(int(rmsb, 2))
            binary = binary[bits_to_read:]
        return doc_ids

    def read_posting_gamma(self, term, vocabulary, dgaps=False):
        with open(BIN_INVERTED_INDEX_GAMMA_FILEPATH, "rb") as f:
            try:
                df, index_pointer, gamma_pointer, gamma_bits, gamma_frequencies_len, variable_pointer, variable_bits, variable_frequencies_len = vocabulary[term]
            except:
                return []
            f.seek(gamma_pointer)

            rest = (gamma_bits % 8)
            if rest != 0:
                padding = 8 - rest
            else:
                padding = 0

            data = f.read((gamma_bits + padding) // 8)
            doc_ids = self.decompress_gamma(data, padding)

            frequencies = f.read(gamma_frequencies_len // 8)
            frequencies = self.decompress_frequencies(frequencies, len(doc_ids))
            postings_lists = []
            last_doc_id = 0
            for i in range(len(doc_ids)):
                if dgaps:
                    postings_lists.append([doc_ids[i]+last_doc_id, frequencies[i]])
                    last_doc_id = doc_ids[i]
                else:
                    postings_lists.append([doc_ids[i], frequencies[i]])

            return postings_lists

    def read_posting(self, term, vocabulary, dgaps=False):
        with open(BIN_INVERTED_INDEX_FILEPATH, "rb") as f:
            try:
                df, index_pointer, gamma_pointer, gamma_bits, gamma_frequencies_len, variable_pointer, variable_bits, variable_frequencies_len = vocabulary[term]
            except:
                return []

            entry_string_format = "IHxx"
            complete_string_format = entry_string_format*df
            f.seek(index_pointer)
            content = f.read(struct.calcsize(complete_string_format))
            unpacked_data = struct.unpack(complete_string_format, content)

            postings_lists = []
            i = 0
            last_doc_id = 0
            while i < len(unpacked_data):
                if dgaps:
                    postings_lists.append([unpacked_data[i]+last_doc_id, unpacked_data[i+1]])
                    last_doc_id = unpacked_data[i]
                else:
                    postings_lists.append([unpacked_data[i], unpacked_data[i+1]])
                i += 2
            return postings_lists
