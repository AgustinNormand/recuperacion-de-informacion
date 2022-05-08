import struct
import matplotlib.pyplot as plt
import os
import constants as c

class Exporter:
    def save_docnames_ids_file(self, docnames_ids):
        docnames_ids_list = [(bytes(k, "utf-8"), v) for k, v in docnames_ids.items()]
        string_format = "{}s{}I".format(c.DOCNAMES_SIZE, 1)
        with open(c.INDEX_FILES_PATH + c.BIN_DOCNAMES_IDS_FILENAME, "wb") as f:
            for value in docnames_ids_list:
                packed_data = struct.pack(string_format, *value)
                f.write(packed_data)
                
        with open(c.HUMAN_FILES_PATH + c.TXT_DOCNAMES_IDS_FILENAME, "w") as f:
            f.write("{}\t{}\r\n".format("doc_name", "id"))
            for doc_id in docnames_ids:
                f.write("{}\t{}\r\n".format(doc_id, docnames_ids[doc_id]))

    def inverted_index(self, inverted_index):
        with open(c.INDEX_FILES_PATH + c.BIN_INVERTED_INDEX_FILENAME, "wb") as f:
            for key in inverted_index:
                string_format = "{}I".format(len(inverted_index[key]))
                packed_data = struct.pack(string_format, *inverted_index[key])
                f.write(packed_data)

        with open(c.HUMAN_FILES_PATH + c.TXT_INVERTED_INDEX_FILENAME, "w") as f:
            f.write("{}\t{}\r\n".format("term", "[doc_id]"))
            for key in inverted_index:
                f.write("{}\t{}\r\n".format(key, inverted_index[key]))

    def vocabulary_file(self, vocabulary):
        string_format = "{}s{}I{}I".format(c.TERMS_SIZE, 1, 1)
        last_df = 0
        with open(c.INDEX_FILES_PATH + c.BIN_VOCABULARY_FILENAME, "wb") as f:
            for key in vocabulary:
                packed_data = struct.pack(
                    string_format, bytes(key, "utf-8"), vocabulary[key], last_df
                )
                f.write(packed_data)
                last_df += vocabulary[key]

        with open(c.HUMAN_FILES_PATH + c.TXT_VOCABULARY_FILENAME, "w") as f:
            f.write("{}\t{}\r\n".format("term", "[df]"))
            for value in vocabulary:
                f.write("{}\t{}\r\n".format(value, vocabulary[value]))
