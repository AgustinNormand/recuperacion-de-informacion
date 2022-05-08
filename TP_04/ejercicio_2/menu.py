import sys
sys.path.append('../ejercicio_1/script_1')
from retrieval import Retrieval
from constants import *

def mostrar_menu_configuracion():
    #print("python3 menu.py <path archivo palabras vacias>\r\n")
    print("python3 menu.py <extract_entities> <stemming_language> \r\n")
    print("Verifique los parámetros. \r\n")
    print("Stemming Language: {}".format(STEM))
    print("Extract Entities: {}".format(EXTRACT_ENTITIES))
    print("\r\n")
    mostrar_menu_principal()

def mostrar_menu_principal():
    r = Retrieval(True)

    print('Ingrese la query')
    user_input = input()
    for document_id in r.query(user_input):
        print(document_id)

mostrar_menu_configuracion()

# john|cdata
# LONG LIST

# john|cdata
# Empty

