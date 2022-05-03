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
id_in_docname = False
html_files = False

if len(sys.argv) > 1:
    dirpath = sys.argv[1]

if len(sys.argv) > 2:
    empty_words_path = sys.argv[2]

if len(sys.argv) > 3:
    stemming_language = sys.argv[3].lower()

if len(sys.argv) > 4:
    extract_entities = strtobool(sys.argv[4])

if len(sys.argv) > 5:
    id_in_docname = strtobool(sys.argv[5])

if len(sys.argv) > 6:
    html_files = strtobool(sys.argv[6])

def mostrar_menu_configuracion():
    print("python3 menu.py <path_corpus> <path archivo palabras vacias> <stemming_language> <extract_entities> <id_in_docname> <html_files> \r\n")
    print("Verifique los parámetros. \r\n")
    print("Path de la colección: {}".format(dirpath))
    print("Path del archivo de palabras vacias: {}".format(empty_words_path))
    print("Stemming Language: {}".format(stemming_language))
    print("Extract Entities: {}".format(extract_entities))
    print("Id in docname (docNN.txt):  {}".format(id_in_docname))
    print("HTML files: {}".format(html_files))
    mostrar_menu_principal()

def mostrar_menu_principal():
    print("\r\n")
    Indexer(dirpath, empty_words_path, stemming_language, extract_entities, id_in_docname, html_files)

mostrar_menu_configuracion()
