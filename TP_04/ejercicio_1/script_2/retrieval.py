from importer import Importer
import struct
from normalizer import Normalizer

class Retrieval():
    def __init__(self):
        self.importer = Importer()
        self.vocabulary = self.importer.read_vocabulary("../script_1/output/vocabulary.bin")
        self.normalizer = Normalizer()

    def get_posting(self, term):
        normalized_term = self.normalizer.normalize(term)
        with open("../script_1/output/inverted_index.bin", "rb") as f:
            df, pointer = self.vocabulary[normalized_term]
            string_format = "{}I".format(df)

            f.seek(pointer*struct.calcsize("I"))
            content = f.read(struct.calcsize(string_format))
            unpacked_data = struct.unpack(string_format, content)
            
            return list(unpacked_data)

