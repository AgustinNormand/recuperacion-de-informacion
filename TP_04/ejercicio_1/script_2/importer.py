import struct
from constants import *
class Importer:

    def read_vocabulary(self, filepath):
        with open(filepath, "rb") as f:
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