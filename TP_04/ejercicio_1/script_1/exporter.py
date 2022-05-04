import struct
import matplotlib.pyplot as plt
import os
import constants as c


class Exporter:
    def document_overhead(self, docnames_ids, inverted_index):
        #acum = 0
        docid_overhead = {}
        overhead_count = {}
        for key in docnames_ids.keys():
            file_size = os.path.getsize(key)
            #print("File size: {} bytes".format(file_size))
            file_id = docnames_ids[key]
            counter = 0
            for key in inverted_index:
                if file_id in inverted_index[key]:
                    counter += 1
            #print("{} times had to save id in posting".format(counter))
            #print("1 time had to save id in docnames_ids.bin")
            #print("{} characters used for the title".format(115))#FIXME NO DEBERIA ESTAR HARDCODEADO
            total_size = counter*4+4+c.DOCNAMES_SIZE
            overhead = total_size/(total_size+file_size)
            docid_overhead[file_id] = overhead
            try:
                overhead_count[round(overhead, 2)] += 1
            except:
                overhead_count[round(overhead, 2)] = 1
            #print("Total size: {} bytes".format(total_size))
            #acum += total_size
        #print("Acum: {}".format(acum))
        #print(docid_overhead)
        keys = sorted(overhead_count.keys())
        #print(keys)
        values = []
        for key in keys:
            values.append(overhead_count[key])

        plt.figure(0)
        plt.plot(keys, values)
        #plt.xlim(min(keys), max(keys))
        #plt.ylim(min(values), max(values))
        plt.xlabel('Overhead')
        plt.ylabel('Cantidad de documentos')
        plt.savefig(c.OVERHEAD_PLOT_PATH)
        #print(overhead_count)

    def get_size(self, directory):
        size = 0
        for path, dirs, files in os.walk(directory):
            for f in files:
                fp = os.path.join(path, f)
                size += os.path.getsize(fp)
        return size

    def collection_overhead(self):
        corpus_size = self.get_size(c.DIRPATH)
        index_size = self.get_size(c.INDEX_FILES_PATH)
        
        print("Corpus Size: {} bytes, Index Size: {} bytes".format(corpus_size, index_size))
        print("Overhead: {}".format(index_size/(corpus_size+index_size)))


    def postings_distribution(self, inverted_index):
        distribution = {}
        for value in inverted_index:
            try:
                distribution[len(inverted_index[value])*4] += 1
            except:
                distribution[len(inverted_index[value])*4] = 1
        
        keys = sorted(distribution.keys())
        values = []
        for key in keys:
            values.append(distribution[key])

        plt.figure(1)
        plt.plot(keys, values)
        #plt.xlim(min(keys), max(keys))
        #plt.ylim(min(values), max(values))
        plt.xlabel('Bytes')
        plt.ylabel('Cantidad de postings')
        plt.savefig(c.POSTINGS_PLOT_PATH)

    def get_max_length(self, array):
        max_length = 0
        for value in array:
            if len(value) > max_length:
                max_length = len(value)
        return max_length

    def set_docnames_ids_file(self, docnames_ids):
        docnames_ids_list = [(bytes(k, 'utf-8'), v) for k, v in docnames_ids.items()]
        max_length = self.get_max_length(docnames_ids.keys())
        print("Max length docnames_ids: {}. Actual length: {}.".format(max_length, c.DOCNAMES_SIZE)) #TODO
        string_format = "{}s{}I".format(c.DOCNAMES_SIZE, 1)
        with open(c.INDEX_FILES_PATH+c.DOCNAMES_IDS_FILENAME+".bin", 'wb') as f:
            for value in docnames_ids_list:
                packed_data = struct.pack(string_format, *value)
                f.write(packed_data)
                #print(binascii.hexlify(packed_data))
        # Mejorar y no hacer escrituras repetidas, sino una sola escritura.    

        #Mejorar, no usar el path absoluto. Incluso, no usar docNN.txt, solo almacenar el NN

        with open(c.HUMAN_FILES_PATH+c.DOCNAMES_IDS_FILENAME+".txt", "w") as f:
            f.write("{}\t{}\r\n".format("doc_name", "id"))
            for doc_id in docnames_ids:
                f.write("{}\t{}\r\n".format(doc_id, docnames_ids[doc_id]))
                
    def inverted_index(self, inverted_index):
        with open(c.INDEX_FILES_PATH+c.INVERTED_INDEX_FILENAME+".bin", 'wb') as f:
            for key in inverted_index:
                string_format = "{}I".format(len(inverted_index[key]))
                packed_data = struct.pack(string_format, *inverted_index[key])
                f.write(packed_data)

        with open(c.HUMAN_FILES_PATH+c.INVERTED_INDEX_FILENAME+".txt", "w") as f:
            f.write("{}\t{}\r\n".format(
                "term", "[doc_id]"))
            for key in inverted_index:
                f.write("{}\t{}\r\n".format(key, inverted_index[key]))

    def vocabulary_file(self, vocabulary):
        max_length = self.get_max_length(vocabulary.keys())
        print("Max length vocabulary: {}. Actual length: {}.".format(max_length, c.TERMS_SIZE)) #TODO
        string_format = "{}s{}I{}I".format(c.TERMS_SIZE, 1, 1) #Esto debería coincidir con el paramtro del tokenizer
        last_df = 0
        with open(c.INDEX_FILES_PATH+c.VOCABULARY_FILENAME+".bin", 'wb') as f:
            for key in vocabulary:
                packed_data = struct.pack(string_format, bytes(key, 'utf-8'), vocabulary[key], last_df)
                #print(binascii.hexlify(packed_data))
                f.write(packed_data)
                last_df += vocabulary[key]
        # Mejorar el tamaño del string para los terminos
            
        with open(c.HUMAN_FILES_PATH+c.VOCABULARY_FILENAME+".txt", "w") as f:
                f.write("{}\t{}\r\n".format('term', "[df]"))
                for value in vocabulary:
                    f.write("{}\t{}\r\n".format(value, vocabulary[value]))