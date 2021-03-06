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
    results = r.query(user_input)
    for doc_id in results:
        print("{} {}".format(doc_id, results[doc_id]))

mostrar_menu_configuracion()
