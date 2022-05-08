from constants import *
import pathlib

#import sys
#sys.path.append('../ejercicio_1/script_1')

from normalizer import *

class Indexer:
    def __init__(self):
        self.load_documents()
        self.normalizer = Normalizer()
        self.index()
        
    def load_documents(self):
        corpus_path = pathlib.Path(DIRPATH)
        self.docnames_ids = {}
        id_count = 0
        for file_name in corpus_path.rglob("*.*"): 
            id_count += 1
            doc_id = id_count
            self.docnames_ids[str(file_name.resolve())] = doc_id
        print("10% of collection: {}".format(round(0.1*id_count)))

    def index(self):
        for value in self.docnames_ids:
            with open(value, "r", encoding="ISO-8859-1") as f:
                for line in f.readlines():
                    for word in line.split():
                        token = self.normalizer.normalize(word)
                        print(token)