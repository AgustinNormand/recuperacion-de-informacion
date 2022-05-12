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

    def ids_norm(self, index):
        with open(BIN_NORM_FILEPATH, "wb") as f:
            for doc_id in index:
                acum = 0
                for term in index[doc_id]:
                    frequency = index[doc_id][term]
                    acum += math.pow(frequency, 2)
                document_norm = math.sqrt(acum)
                entry_string_format = "If"
                packed_data = struct.pack(entry_string_format, doc_id, document_norm)
                f.write(packed_data)

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
"""
    def export_statistics(
        self, array, name, actual_length, xlabel, ylabel, plot_path, figure_number
    ):
        acum = 0
        counter = 0
        max_length = 0
        lengths = []
        for key in array:
            length = len(key)
            acum += length
            counter += 1
            if length > max_length:
                max_length = length
            lengths.append(length)
        print("\r")
        print("{} mean length: {}".format(name, acum / counter))
        print("{} max length: {}".format(name, max_length))
        print("{} actual length: {}".format(name, max_length))

        plt.figure(figure_number)
        plt.hist(lengths)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.axvline(actual_length, color="k", linestyle="dashed", linewidth=1)
        plt.savefig(plot_path)
        print("{} length distribution plot exported".format(name))

    def export_all_statistics(self):
        self.collection_overhead()
        self.postings_distribution()
        self.document_overhead()
        self.export_statistics(
            self.docnames_ids.keys(),
            "Document titles",
            self.docnames_size,
            "Longitud del titulo",
            "Cantidad de documentos",
            "./human_files/title_length.png",
            2)
        self.export_statistics(
            self.vocabulary.keys(),
            "Terms",
            self.terms_size,
            "x",
            "y",
            "./human_files/term_length.png",
            3,
        )

    def document_overhead(self):
        docid_overhead = {}
        overhead_count = {}
        for key in self.docnames_ids.keys():
            file_size = os.path.getsize(key)
            file_id = self.docnames_ids[key]
            counter = 0
            for key in self.inverted_index:
                if file_id in self.inverted_index[key]:
                    counter += 1
            total_size = counter * 4 + 4 + self.docnames_size + (2+2)
            overhead = total_size / (total_size + file_size)
            docid_overhead[file_id] = overhead
            try:
                overhead_count[round(overhead, 2)] += 1
            except:
                overhead_count[round(overhead, 2)] = 1
        keys = sorted(overhead_count.keys())
        values = []
        for key in keys:
            values.append(overhead_count[key])

        plt.figure(0)
        plt.plot(keys, values)
        plt.xlabel("Overhead")
        plt.ylabel("Cantidad de documentos")
        plt.savefig("./human_files/documents_overhead.png")

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

    def postings_distribution(self):
        distribution = {}
        for value in self.inverted_index:
            try:
                distribution[len(self.inverted_index[value]) * 4] += 1
            except:
                distribution[len(self.inverted_index[value]) * 4] = 1

        keys = sorted(distribution.keys())
        values = []
        for key in keys:
            values.append(distribution[key])

        plt.figure(1)
        plt.plot(keys, values)
        plt.xlabel("Bytes")
        plt.ylabel("Cantidad de postings")
        plt.savefig("./human_files/postings_distribution.png")

"""