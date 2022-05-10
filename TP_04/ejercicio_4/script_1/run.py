from fileinput import filename
from indexer import *
import constants as c
import os

parts_path = pathlib.Path(PART_INVERTED_INDEX_PATH)
for file_name in parts_path.iterdir():
    os.remove(file_name)

def mostrar_menu_configuracion():
    print("Verifique los parámetros: \r")
    print("Path de la colección: {}".format(c.DIRPATH))
    print("Path del archivo de palabras vacias: {}".format(c.EMPTY_WORDS_PATH))
    print("Stemming Language: {}".format(c.STEMMING_LANGUAGE))
    print("Extract Entities: {}".format(c.EXTRACT_ENTITIES))
    print("Id in docname (docNN.txt): {}".format(c.ID_IN_DOCNAME))
    print("Cantidad de threads: {}".format(c.WORKERS_NUMBER))
    mostrar_menu_principal()

def mostrar_menu_principal():
    Indexer()

mostrar_menu_configuracion()
