import pickle


class Exporter:
    def docnames_ids_file(self, docnames_ids, filepath):
        with open(filepath+".pkl", 'wb') as f:
            pickle.dump(docnames_ids, f)

        with open(filepath+".txt", "w") as f:
            f.write("{}\t{}\r\n".format("doc_name", "id"))
            for doc_id in docnames_ids:
                f.write("{}\t{}\r\n".format(doc_id, docnames_ids[doc_id]))

    def inverted_index(self, inverted_index, filepath):
        with open(filepath+".pkl", 'wb') as f:
            pickle.dump(inverted_index, f)

        with open(filepath+".txt", "w") as f:
            f.write("{}\t{}\r\n".format(
                "term", "[doc_id, frequency]"))
            for key in inverted_index:
                f.write("{}\t{}\r\n".format(key, inverted_index[key]))

    def vocabulary_file(self, vocabulary, filepath):
        with open(filepath+".pkl", 'wb') as f:
            pickle.dump(vocabulary, f)

        with open(filepath+".txt", "w") as f:
            f.write("{}\t{}\r\n".format('term', "[df, idf]"))
            for value in vocabulary:
                f.write("{}\t{}\r\n".format(value, vocabulary[value]))

    def documents_vectors(self, documents_vectors, filepath):
        with open(filepath+".pkl", 'wb') as f:
            pickle.dump(documents_vectors, f)

        with open(filepath+".txt", "w") as f:
            f.write("{}\t{}\r\n".format('doc_id', "{term: TF}"))
            for value in documents_vectors:
                f.write("{}\t{}\r\n".format(value, documents_vectors[value]))

    def documents_norm(self, documents_norm, filepath):
        with open(filepath+".pkl", 'wb') as f:
            pickle.dump(documents_norm, f)

        with open(filepath+".txt", "w") as f:
            f.write("{}\t{}\r\n".format('doc_id', "norm"))
            for value in documents_norm:
                f.write("{}\t{}\r\n".format(value, documents_norm[value]))
