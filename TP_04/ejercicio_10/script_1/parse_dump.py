from constants import *
from exporter import *


vocabulary = {}
inverted_index = {}
with open(DUMP_10K_FILE, "r") as f:
    for line in f.readlines():
        term, df, doc_ids = line.split(":")
        doc_ids = doc_ids.strip().split(",")
        if doc_ids[len(doc_ids)-1] == "":
            doc_ids = doc_ids[:len(doc_ids)-1]

        vocabulary[term] = int(df)
        inverted_index[term] = sorted(list(map(int, doc_ids)))

exporter = Exporter()
exporter.inverted_index(inverted_index)
exporter.vocabulary_file(vocabulary)
exporter.metadata()