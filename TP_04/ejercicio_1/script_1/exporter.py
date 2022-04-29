import struct
import binascii

class Exporter:
    def set_docnames_ids_file(self, docnames_ids, filepath):
        docnames_ids_list = [(bytes(k, 'utf-8'), v) for k, v in docnames_ids.items()]
        string_format = "{}s{}I".format(100, 1)
        with open(filepath+".bin", 'wb') as f:
            for value in docnames_ids_list:
                packed_data = struct.pack(string_format, *value)
                f.write(packed_data)
                #print(binascii.hexlify(packed_data))
        # Mejorar y no hacer escrituras repetidas, sino una sola escritura.    

        """
        with open(filepath+".txt", "w") as f:
            f.write("{}\t{}\r\n".format("doc_name", "id"))
            for doc_id in docnames_ids:
                f.write("{}\t{}\r\n".format(doc_id, docnames_ids[doc_id]))
        """
                
    def inverted_index(self, inverted_index, filepath):
        with open(filepath+".bin", 'wb') as f:
            for key in inverted_index:
                string_format = "{}I".format(len(inverted_index[key]))
                packed_data = struct.pack(string_format, *inverted_index[key])
                f.write(packed_data)

        """
        with open(filepath+".txt", "w") as f:
            f.write("{}\t{}\r\n".format(
                "term", "[doc_id]"))
            for key in inverted_index:
                f.write("{}\t{}\r\n".format(key, inverted_index[key]))
        """

    def vocabulary_file(self, vocabulary, filepath):
        string_format = "{}s{}I{}I".format(20, 1, 1) #Esto debería coincidir con el paramtro del tokenizer
        last_df = 0
        with open(filepath+".bin", 'wb') as f:
            for key in vocabulary:
                packed_data = struct.pack(string_format, bytes(key, 'utf-8'), vocabulary[key], last_df)
                #print(binascii.hexlify(packed_data))
                f.write(packed_data)
                last_df += vocabulary[key]
        # Mejorar el tamaño del string para los terminos
            
        """
        with open(filepath+".txt", "w") as f:
                f.write("{}\t{}\r\n".format('term', "[df]"))
                for value in vocabulary:
                    f.write("{}\t{}\r\n".format(value, vocabulary[value]))
        """