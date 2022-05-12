import struct
import matplotlib.pyplot as plt
import os
from constants import *
import json

class Exporter:
    ## Document Titles
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
        with open(INDEX_FILES_PATH + BIN_DOCNAMES_IDS_FILENAME, "wb") as f:
            for value in docnames_ids_list:
                packed_data = struct.pack(string_format, *value)
                f.write(packed_data)
    ##

    ## Inverted Index

    def inverted_index(self, inverted_index):
        #print("Inverted Index:")
        #print(inverted_index)
        self.inverted_index_pointers = {}
        self.skips_pointers = {}
        inverted_index_string_format = "I"
        skips_string_format = "II"
        #Debería ser un byte el puntero, y para que sea mas chico, no calcularlo
        #Si no los multiplico por el calcsize, son numeros mas chicos, se pueden comprimir mejor
        inverted_index_file = open(INDEX_FILES_PATH + BIN_INVERTED_INDEX_FILENAME, "wb")
        skips = open(INDEX_FILES_PATH + BIN_SKIPS_FILENAME, "wb")
        inverted_index_pointer_acumulator = 0
        skips_pointer_acumulator = 0
        
        for key in inverted_index:
            #print("Key {} {}".format(key, inverted_index[key]))
            #print("Start in inverted index: {}".format(inverted_index_pointer_acumulator))
            #print("Start in skips: {}".format(skips_pointer_acumulator))
            self.inverted_index_pointers[key] = inverted_index_pointer_acumulator
            self.skips_pointers[key] = skips_pointer_acumulator

            #No es asi#doc_ids_writed = 2 #Para que el primero que escriba, lo incremente, y guarde la skip
            doc_ids_writed = 0
            posting = inverted_index[key]
            for doc_id in posting:
                packed_data = struct.pack(inverted_index_string_format, doc_id)
                inverted_index_file.write(packed_data)
                doc_ids_writed += 1
                if doc_ids_writed == K_SKIPS:
                    packed_data = struct.pack(skips_string_format, doc_id, inverted_index_pointer_acumulator)
                    skips.write(packed_data)
                    doc_ids_writed = 0
                    skips_pointer_acumulator += struct.calcsize(skips_string_format)
                inverted_index_pointer_acumulator += struct.calcsize(inverted_index_string_format)

        #print(self.skips_pointers)
    ##

    ## Vocabulary

    def analize_terms_length(self, vocabulary):
        if STRING_STORE_CRITERION == "MAX":
            self.terms_size = self.get_max_length(vocabulary.keys())
        else:
            self.terms_size = TERMS_SIZE

    def vocabulary_file(self, vocabulary):
        
        self.analize_terms_length(vocabulary)
        string_format = "{}sIII".format(self.terms_size)
        with open(INDEX_FILES_PATH + BIN_VOCABULARY_FILENAME, "wb") as f:
            for key in vocabulary:
                packed_data = struct.pack(
                    string_format, bytes(key, "utf-8"), vocabulary[key], self.skips_pointers[key], self.inverted_index_pointers[key]
                )
                f.write(packed_data)

    ##

    def metadata(self):
        metadata = {}
        metadata["DOCNAMES_SIZE"] = self.docnames_size
        metadata["TERMS_SIZE"] = self.terms_size
        metadata["STEMMING_LANGUAGE"] = STEMMING_LANGUAGE
        metadata["EXTRACT_ENTITIES"] = EXTRACT_ENTITIES
        with open(INDEX_FILES_PATH+METADATA_FILE, 'w') as fp:
            json.dump(metadata, fp,  indent=4)

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

        if PLOT_RESULTS:
            plt.figure(figure_number)
            plt.hist(lengths)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.axvline(actual_length, color="k", linestyle="dashed", linewidth=1)
            plt.savefig(plot_path)
            print("{} length distribution plot exported".format(name))

    def document_overhead(self, docnames_ids, inverted_index):
        docid_overhead = {}
        overhead_count = {}
        for key in docnames_ids.keys():
            file_size = os.path.getsize(key)
            file_id = docnames_ids[key]
            counter = 0
            for key in inverted_index:
                if file_id in inverted_index[key]:
                    counter += 1
            total_size = counter * 4 + 4 + DOCNAMES_SIZE
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

        if PLOT_RESULTS:
            plt.figure(0)
            plt.plot(keys, values)
            plt.xlabel("Overhead")
            plt.ylabel("Cantidad de documentos")
            plt.savefig(OVERHEAD_PLOT_PATH)

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

    def postings_distribution(self, inverted_index):
        distribution = {}
        for value in inverted_index:
            try:
                distribution[len(inverted_index[value]) * 4] += 1
            except:
                distribution[len(inverted_index[value]) * 4] = 1

        keys = sorted(distribution.keys())
        values = []
        for key in keys:
            values.append(distribution[key])

        if PLOT_RESULTS:
            plt.figure(1)
            plt.plot(keys, values)
            plt.xlabel("Bytes")
            plt.ylabel("Cantidad de postings")
            plt.savefig(POSTINGS_PLOT_PATH)

    """