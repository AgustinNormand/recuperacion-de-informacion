import struct
import matplotlib.pyplot as plt
import os
from constants import *
import json
from constants import *
import binascii
import pathlib


class Exporter:
    def __init__(self):
        self.pointers = {}

    def metadata(self):
        metadata = {}
        metadata["DOCNAMES_SIZE"] = self.docnames_size
        metadata["TERMS_SIZE"] = self.terms_size
        metadata["STEMMING_LANGUAGE"] = STEMMING_LANGUAGE
        metadata["EXTRACT_ENTITIES"] = EXTRACT_ENTITIES
        with open(INDEX_FILES_PATH + METADATA_FILE, "w") as fp:
            json.dump(metadata, fp, indent=4)

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
        # Mejorar y no hacer escrituras repetidas, sino una sola escritura.
        # Incluso, no usar docNN.txt, solo almacenar el NN


    def compute_vocabulary(self):
        self.vocabulary = {}
        for key in self.pointers:
            for term in self.pointers[key]:
                self.vocabulary[term] = 0
                    


    def save_process_block(
        self, partial_inverted_index, worker_number, process_block_count
    ):
        process_block_pointers = {}
        filename = "worker_number_{}_process_block_{}.bin".format(
            worker_number, process_block_count
        )
        part_path = PART_INVERTED_INDEX_PATH + filename
        pointer = 0
        with open(part_path, "wb") as f:
            for key in partial_inverted_index:
                process_block_pointers[key] = [pointer, len(partial_inverted_index[key])]
                string_format = "{}I".format(len(partial_inverted_index[key]))
                packed_data = struct.pack(string_format, *partial_inverted_index[key])
                
                f.write(packed_data)
                pointer += struct.calcsize(string_format)
        self.pointers[filename] = process_block_pointers

    def read_posting(self, filepath, df, pointer):
        with open(filepath, "rb") as f:
            entry_string_format = "I"
            complete_string_format = entry_string_format*df
            f.seek(pointer)
            content = f.read(struct.calcsize(complete_string_format))
            unpacked_data = struct.unpack(complete_string_format, content)
            return unpacked_data


    def merge_inverted_index(self):
        parts_path = pathlib.Path(PART_INVERTED_INDEX_PATH)
        part_files = {}
        for file_name in parts_path.iterdir():
            process_block_number = int(file_name.stem.split("process_block_")[1])
            part_files[process_block_number] = file_name

        self.final_pointers = {}
        pointer_acumulator = 0
        with open(INDEX_FILES_PATH + BIN_INVERTED_INDEX_FILENAME, "wb") as f:
            for key in self.vocabulary:
                #print("La clave {}".format(key))
                final_posting_list = []
                for i in range(len(part_files)):
                    filename = part_files[i]
                    
                    # Si el termino que estoy reconstruyendo el indice, no está en el archivo, sigo
                    if key not in self.pointers[filename.name].keys():
                        continue
                    pointer, df = self.pointers[filename.name][key]
                    #print("En el archivo {}, el puntero es {}, y hay que leer {} docids".format(filename, pointer, df))
                    #print(self.read_posting(filename, df, pointer))
                    final_posting_list.extend(list(self.read_posting(filename, df, pointer)))
                string_format = "{}I".format(len(final_posting_list))
                packed_data = struct.pack(string_format, *final_posting_list)
                f.write(packed_data)
                self.final_pointers[key] = pointer_acumulator
                pointer_acumulator += len(final_posting_list)
                self.vocabulary[key] = len(final_posting_list)

        
    def analize_terms_length(self, vocabulary):
        if STRING_STORE_CRITERION == "MAX":
            self.terms_size = self.get_max_length(vocabulary)
        else:
            self.terms_size = TERMS_SIZE

    def vocabulary_file(self):
        self.analize_terms_length(self.vocabulary.keys())
        string_format = "{}s{}I{}I".format(self.terms_size, 1, 1)
        with open(INDEX_FILES_PATH + BIN_VOCABULARY_FILENAME, "wb") as f:
            for key in self.vocabulary:
                packed_data = struct.pack(
                    string_format, bytes(key, "utf-8"), self.vocabulary[key], self.final_pointers[key]
                )
                f.write(packed_data)