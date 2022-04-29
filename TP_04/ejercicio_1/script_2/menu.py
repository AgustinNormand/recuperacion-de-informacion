import sys

from retrieval import Retrieval

empty_words_path = None

if len(sys.argv) > 1:
    empty_words_path = sys.argv[1]

def mostrar_menu_configuracion():
    print("python3 menu.py <path archivo palabras vacias>\r\n")
    print("Verifique los parámetros. \r\n")
    print("Path del archivo de palabras vacias: {}".format(empty_words_path))
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
