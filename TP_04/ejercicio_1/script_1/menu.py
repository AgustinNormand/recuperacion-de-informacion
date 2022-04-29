from indexer import Indexer
import sys

dirpath = None
empty_words_path = None

if len(sys.argv) > 1:
    dirpath = sys.argv[1]

if len(sys.argv) > 2:
    empty_words_path = sys.argv[2]


def mostrar_menu_configuracion():
    print("python3 menu.py <path_corpus> <0 usar indice de disco, 1 volver a indexar> <path archivo palabras vacias>\r\n")
    print("Verifique los parámetros. \r\n")
    print("Path de la colección: {}".format(dirpath))
    print("Path del archivo de palabras vacias: {}".format(empty_words_path))
    mostrar_menu_principal()

def mostrar_menu_principal():
    print("\r\n")
    Indexer(dirpath, empty_words_path)

mostrar_menu_configuracion()
