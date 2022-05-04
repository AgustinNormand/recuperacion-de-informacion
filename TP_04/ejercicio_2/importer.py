import struct
import binascii

class Importer:

    def read_vocabulary(self, filepath):
        with open(filepath, "rb") as f:
            string_format = "{}s{}I{}I".format(100, 1, 1)
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

    def read_docnames_ids_file(self, filepath):
        ids_docnames = {}
        with open(filepath, "rb") as f:
            string_format = "{}s{}I".format(115, 1)
            read_size = struct.calcsize(string_format)
            content = f.read(read_size)

            while content != b'':
                unpacked_data = struct.unpack(string_format, content) # leo bytes del 
                docname, doc_id = unpacked_data
                #term = str(term, 'utf-8').rstrip('\x00')
                docname = str(docname, 'utf-8').rstrip('\x00')
                ids_docnames[doc_id] = docname
                content = f.read(read_size)
        return ids_docnames


        #docnames_ids_list = [(bytes(k, 'utf-8'), v) for k, v in docnames_ids.items()]
        #max_length = self.get_max_length(docnames_ids.keys())
        #print("Max length docnames_ids: {}".format(max_length)) #TODO
        #string_format = "{}s{}I".format(115, 1)
        #with open("./output/index_files/"+filename+".bin", 'wb') as f:
            #for value in docnames_ids_list:
                #packed_data = struct.pack(string_format, *value)
                #f.write(packed_data)