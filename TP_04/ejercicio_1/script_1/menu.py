from indexer import *
import constants as c

def mostrar_menu_configuracion():
    print("python3 menu.py <path_corpus> <path archivo palabras vacias> <stemming_language> <extract_entities> <id_in_docname> <html_files> \r\n")
    print("Verifique los parámetros: \r")
    print("Path de la colección: {}".format(c.DIRPATH))
    print("Path del archivo de palabras vacias: {}".format(c.EMPTY_WORDS_PATH))
    print("Stemming Language: {}".format(c.STEMMING_LANGUAGE))
    print("Extract Entities: {}".format(c.EXTRACT_ENTITIES))
    print("Id in docname (docNN.txt):  {}".format(c.ID_IN_DOCNAME))
    print("HTML files: {}".format(c.HTML_FILES))
    mostrar_menu_principal()

def mostrar_menu_principal():
    Indexer()

mostrar_menu_configuracion()
