from constants import *
from retrieval import *
import json


def mostrar_menu_configuracion():
    print("Archivo de metadata: {}".format(METADATA_FILE))
    print("\r\n")
    mostrar_menu_principal()

def mostrar_menu_principal():
    metadata = {}
    with open(METADATA_FILE, 'r') as fp:
        metadata = json.load(fp)
    r = Retrieval(metadata)

    print('Ingrese la query')
    user_input = input()
    r.query(user_input)

mostrar_menu_configuracion()
