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

    def analize_terms_length(self, vocabulary):
        if STRING_STORE_CRITERION == "MAX":
            self.terms_size = self.get_max_length(vocabulary.keys())
        else:
            self.terms_size = TERMS_SIZE

    def vocabulary_file(self, vocabulary):
        self.vocabulary = vocabulary
        self.analize_terms_length(vocabulary)
        string_format = "{}s{}I{}I".format(self.terms_size, 1, 1)
        last_df = 0
        with open(INDEX_FILES_PATH + BIN_VOCABULARY_FILENAME, "wb") as f:
            for key in vocabulary:
                packed_data = struct.pack(
                    string_format, bytes(key, "utf-8"), vocabulary[key], last_df
                )
                f.write(packed_data)
                last_df += vocabulary[key]



    def save_process_block(
        self, partial_inverted_index, worker_number, process_block_count
    ):
        #if worker_number == 0:
            #print(partial_inverted_index)
        process_block_pointers = {}
        filename = "worker_number_{}_process_block_{}.bin".format(
            worker_number, process_block_count
        )
        part_path = PART_INVERTED_INDEX_PATH + filename
        pointer = 0
        #spartial_inverted_index = dict(sorted(partial_inverted_index.items(), key=lambda item: item[1]))
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
            #print(binascii.hexlify(content))
            return unpacked_data
            #postings_lists = []
            #i = 0
            #while i < len(unpacked_data):
                #postings_lists.append([unpacked_data[i], unpacked_data[i+1]])
                #i += 2
            #return postings_lists

    def save_posting(self, f, posting):
        string_format = "{}I".format(len(posting))
        packed_data = struct.pack(string_format, *posting)
        f.write(packed_data)
        return len(posting) # A diferencia de save_process_block, dejo el puntero sin calcular, porque el script 2 lo lee asi.

    def merge_inverted_index(self):
        #print(self.vocabulary)
        parts_path = pathlib.Path(PART_INVERTED_INDEX_PATH)
        part_files = {}
        for file_name in parts_path.iterdir():
            process_block_number = int(file_name.stem.split("process_block_")[1])
            part_files[process_block_number] = file_name

        #final_pointers = {}
        #pointer_acumulator = 0
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
                    saved_count = self.save_posting(f, final_posting_list)
                    #final_pointers[key] = pointer_acumulator
                    #pointer_acumulator += saved_count
                #print(final_posting_list)
                #print(final_pointers)
                #print(self.vocabulary[key])
                #break
    # No hago mas nada con los pointers porque cuando guardo el vocabulary, también guardo los pointers, usando el df 
    # de cada término. Como para guardaar el indice final, estoy usando el mismo orden del vocabulary, no hace falta 
    # hacer mas nada       


#{'sra': [0, 14], 'dasmi': [56, 20], 'https://www.researchgate.net/publication/2360239': [136, 100], 'Domingo Faustino Sarmiento': [536, 100], 'lluvi': [936, 30], 'mratto@mail.unlu.edu.ar': [1056, 14], '15413355': [1112, 29], 'abc.def@mail-archive.com': [1228, 9], 'botell': [1264, 17], 'terner': [1332, 38], 'http://www.tcpipguide.com/free/t_TCPIPProcessesMultiplexingandClientServerApplicati.htm': [1484, 11], '2021-12-09': [1528, 13], 'usa': [1580, 3], 'https://www.labredes.unlu.edu.ar/tyr2022': [1592, 5], 'https://docs.google.com/document/d/1ninD55Cfbb_7PksDirN0XghzNHJZ_N93lheQzF1aOZY/edit?usp=sharing': [1612, 12], 'tenis': [1660, 13], 'https://www.youtube.com/watch?v=zKqUfwB84Zg': [1712, 8], 'ftp://unlu.edu.ar': [1744, 4], 'eeuu': [1760, 5]}
