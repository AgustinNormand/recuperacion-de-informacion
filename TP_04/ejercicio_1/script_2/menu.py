from constants import *
from retrieval import *


empty_words_path = EMPTY_WORDS_PATH
stemming_language = STEMMING_LANGUAGE
extract_entities = EXTRACT_ENTITIES

def mostrar_menu_configuracion():
    print("python3 menu.py <extract_entities> <stemming_language> \r\n")
    print("Verifique los parámetros. \r\n")
    print("Stemming Language: {}".format(stemming_language))
    print("Extract Entities: {}".format(extract_entities))
    print("\r\n")
    mostrar_menu_principal()

def mostrar_menu_principal():
    r = Retrieval()

    print('Ingrese el término del cual quiere la posting list')
    user_input = input()
    posting_list = r.get_posting(user_input)
    for posting in posting_list:
        print(posting)

mostrar_menu_configuracion()
