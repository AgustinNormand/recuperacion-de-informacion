import struct
from constants import *
import binascii
#from bitarray import bitarray
from bitstring import BitStream, BitArray

class Importer:

    def __init__(self, terms_size):
        self.terms_size = terms_size

    def read_vocabulary(self):
        with open(BIN_VOCABULARY_FILEPATH, "rb") as f:
            string_format = "{}s6I".format(self.terms_size)
            read_size = struct.calcsize(string_format)
            vocabulary = {}

            content = f.read(read_size)
            while content != b'':
                unpacked_data = struct.unpack(string_format, content)
                term, df, index_pointer, gamma_pointer, gamma_bits, variable_pointer, variable_bits = unpacked_data
                term = str(term, 'utf-8').rstrip('\x00')
                vocabulary[term] = (df, index_pointer, gamma_pointer, gamma_bits, variable_pointer, variable_bits)
                content = f.read(read_size)

        return vocabulary

    def decompress_variable(self, data):
        hexa = binascii.hexlify(data)
        binary = bin(int(hexa, 16)).replace("0b", "")
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

    def read_posting_variable(self, term, vocabulary):

        with open(BIN_INVERTED_INDEX_VARIABLE_FILEPATH, "rb") as f:
            try:
                df, index_pointer, gamma_pointer, gamma_bits, variable_pointer, variable_bits = vocabulary[term]
            except:
                return []
            f.seek(variable_pointer)
            data = f.read(variable_bits // 8)
            doc_ids = self.decompress_variable(data)
            #print(doc_ids)
            return doc_ids

    def decompress_unary(self, data):
        acum = 0
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
            #print("Binary: "+binary)

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
            #print("Unary part: "+unary_part)
            #print("Binary rest: "+binary)
            bits_to_read = self.decompress_unary(unary_part)
            #print("Bits to read: "+str(bits_to_read))
            rmsb = "1"
            for i in range(bits_to_read):
                rmsb += binary[i]
            #print("rmsb: "+rmsb)
            #print("Int: "+str(int(rmsb, 2)))
            doc_ids.append(int(rmsb, 2))
            binary = binary[bits_to_read:]
        return doc_ids


    def read_posting_gamma(self, term, vocabulary):
        with open(BIN_INVERTED_INDEX_GAMMA_FILEPATH, "rb") as f:
            try:
                df, index_pointer, gamma_pointer, gamma_bits, variable_pointer, variable_bits = vocabulary[term]
            except:
                return []
            f.seek(gamma_pointer)
            #print(gamma_bits)

            rest = (gamma_bits % 8)
            if rest != 0:
                padding = 8 - rest
            else:
                padding = 0

            #print((gamma_bits + padding) // 8)
            data = f.read((gamma_bits + padding) // 8)
            #print(data)
            #print()
            #sys.exit()
            #print(data)
            doc_ids = self.decompress_gamma(data, padding)
            #print(doc_ids)
            return doc_ids

    def read_posting(self, term, vocabulary):
        with open(BIN_INVERTED_INDEX_FILEPATH, "rb") as f:
            try:
                df, index_pointer, gamma_pointer, gamma_bits, variable_pointer, variable_bits = vocabulary[term]
            except:
                return []

            entry_string_format = "IHxx"
            #df, pointer = vocabulary[term]
            complete_string_format = entry_string_format*df
            f.seek(index_pointer)
            content = f.read(struct.calcsize(complete_string_format))
            unpacked_data = struct.unpack(complete_string_format, content)

            postings_lists = []
            i = 0
            while i < len(unpacked_data):
                #postings_lists.append([unpacked_data[i], unpacked_data[i+1]])
                postings_lists.append(unpacked_data[i])
                i += 2
            return postings_lists
