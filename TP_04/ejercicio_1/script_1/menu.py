from numpy import extract
from indexer import Indexer
import sys


def strtobool(string):
    string = string.lower()
    if string == "true" or string == "yes" or string == "1" or string == "si":
        return True
    return False

dirpath = None
empty_words_path = None

stemming_language = "spanish"
extract_entities = True

if len(sys.argv) > 1:
    dirpath = sys.argv[1]

if len(sys.argv) > 2:
    empty_words_path = sys.argv[2]

if len(sys.argv) > 3:
    extract_entities = strtobool(sys.argv[3])

if len(sys.argv) > 4:
    stemming_language = sys.argv[4].lower()
    #if stemming_language != "spanish" and stemming_language != "english":
    #    stemming_language = None

def mostrar_menu_configuracion():
    print("python3 menu.py <path_corpus> <path archivo palabras vacias> <extract_entities> <stemming_language> \r\n")
    print("Verifique los parámetros. \r\n")
    print("Path de la colección: {}".format(dirpath))
    print("Path del archivo de palabras vacias: {}".format(empty_words_path))
    print("Stemming Language: {}".format(stemming_language))
    print("Extract Entities: {}".format(extract_entities))
    mostrar_menu_principal()

def mostrar_menu_principal():
    print("\r\n")
    Indexer(dirpath, empty_words_path, stemming_language, extract_entities)

mostrar_menu_configuracion()
