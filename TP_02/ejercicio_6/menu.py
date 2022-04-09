import indexer as indexer
import sys
import pickle
import model as model
from tokenizer import Tokenizer

dirpath = None
empty_words_path = None
re_index = 0
re_index_label = "None"

docnames_ids_filepath = "./output/docnames_ids"
vocabulary_filepath = "./output/vocabulary"
inverted_index_filepath = "./output/inverted_index"
documents_vectors_filepath = "./output/documents_vectors"
documents_norm_filepath = "./output/documents_norm"

if len(sys.argv) > 1:
    dirpath = sys.argv[1]

if len(sys.argv) > 2:
    re_index = int(sys.argv[2])
    re_index_label = "No"
    if re_index == 1:
        re_index_label = "Si"

if len(sys.argv) > 3:
    empty_words_path = sys.argv[3]


def mostrar_menu_configuracion():
    print("python3 menu.py <path_corpus> <0 usar indice de disco, 1 volver a indexar> <path archivo palabras vacias>\r\n")
    print("Verifique los parámetros. \r\n")
    print("Path de la colección: {}".format(dirpath))
    print("Path del archivo de palabras vacias: {}".format(empty_words_path))
    print("Re-construir indice: {}".format(re_index_label))
    print("\r\n")
    user_input = input("Presione enter para continuar, 0 para salir.")
    if user_input == "0":
        sys.exit()
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


def query(model, tokenizer):
    print("\r\n")
    print("Ingrese la query")
    query = input()
    query_terms = tokenizer.tokenize_query(query)
    print("Términos de la query: {}".format(query_terms))
    model.query(query_terms)

    mostrar_sub_menu(model, tokenizer)


def posting(model, tokenizer):
    print("\r\n")
    print("Ingrese el término buscado")
    term = input()
    normalized_term = tokenizer.tokenize_posting(term)
    print("Term: {}, Posting: {}".format(
        normalized_term, model.get_posting(normalized_term)))
    mostrar_sub_menu(model, tokenizer)


def mostrar_sub_menu(model, tokenizer):
    print("\r\n")
    print('Ingrese 1 para hacer querys')
    print("Ingrese 2 para consultar una posting")
    print("Ingrese 0 para salir")
    user_input = input()
    if user_input == "0":
        sys.exit()
    if user_input == "1":
        query(model, tokenizer)
    if user_input == "2":
        posting(model, tokenizer)


def mostrar_menu_principal():
    print("\r\n")
    if re_index == 1:
        docnames_ids, vocabulary, inverted_index, documents_vectors, documents_norm = indexer.index(
            dirpath, empty_words_path)
    else:
        docnames_ids, vocabulary, inverted_index, documents_vectors, documents_norm = load_files()
        print("Files loaded")

    t = Tokenizer(empty_words_path)
    m = model.Model(docnames_ids, vocabulary, inverted_index,
                    documents_vectors, documents_norm)

    mostrar_sub_menu(m, t)


mostrar_menu_configuracion()  # Comentar esto hace que sea mas rapido el develop
# mostrar_menu_principal()
