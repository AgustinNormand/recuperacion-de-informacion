import sys
import pickle
import model as model
from tokenizer import Tokenizer
import xml.etree.ElementTree as ElementTree

dirpath = None
empty_words_path = None

docnames_ids_filepath = "./output/docnames_ids"
vocabulary_filepath = "./output/vocabulary"
inverted_index_filepath = "./output/inverted_index"
documents_vectors_filepath = "./output/documents_vectors"
documents_norm_filepath = "./output/documents_norm"

if len(sys.argv) <= 1:
    print("Debe ingresar el path al archivo de querys.")
    sys.exit()
    
querys_path = sys.argv[1]

def mostrar_menu_configuracion():
    print("python3 menu.py <path_query>\r\n")
    print("Verifique los parámetros. \r\n")
    print("Archivo de querys: {}".format(querys_path))
    print("\r\n")
    mostrar_menu_principal()


def load_files():
    with open(docnames_ids_filepath+".pkl", 'rb') as f:
        docnames_ids = pickle.load(f)

    with open(vocabulary_filepath+".pkl", 'rb') as f:
        vocabulary = pickle.load(f)

    with open(inverted_index_filepath+".pkl", 'rb') as f:
        inverted_index = pickle.load(f)

    with open(documents_vectors_filepath+".pkl", 'rb') as f:
        documents_vectors = pickle.load(f)

    with open(documents_norm_filepath+".pkl", 'rb') as f:
        documents_norm = pickle.load(f)

    return [docnames_ids, vocabulary, inverted_index, documents_vectors, documents_norm]


def parsear_archivo_querys(filepath):
    querys = []
    with open(filepath, "r") as f:
        read_next = False
        for line in f.readlines():
            if "<title>" in line:
                read_next = True
                continue
            if read_next:
                querys.append(line)
                read_next = False
    return querys

def mostrar_menu_principal():
    print("\r\n")
    docnames_ids, vocabulary, inverted_index, documents_vectors, documents_norm = load_files()

    t = Tokenizer(empty_words_path)
    m = model.Model(docnames_ids, vocabulary, inverted_index,
                    documents_vectors, documents_norm)

    querys = parsear_archivo_querys(querys_path)

    with open("TF_IDF.res", "w") as f:
        query_number = 1
        for query in querys:
            document_count = 0
            retrieved_documents = m.query(t.tokenize_query(query))
            for document_id, score, path in retrieved_documents:
                document_count += 1
                #print(document_id)
                #break
                f.write("{} Q0 d{} {} {} TF_IDF\r\n".format(query_number, document_id, document_count, score))
            #break
            query_number += 1



mostrar_menu_configuracion()  
