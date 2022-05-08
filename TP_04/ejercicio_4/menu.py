from indexer import *
from constants import *

def mostrar_menu_configuracion():
    print("python3 menu.py <path_corpus> <path archivo palabras vacias> <stemming_language> <extract_entities> <id_in_docname> <html_files> \r\n")
    print("Verifique los parámetros: \r")
    print("Path de la colección: {}".format(DIRPATH))
    print("Path del archivo de palabras vacias: {}".format(EMPTY_WORDS_PATH))
    print("Stemming Language: {}".format(STEMMING_LANGUAGE))
    mostrar_menu_principal()

def mostrar_menu_principal():
    Indexer()

mostrar_menu_configuracion()
