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
    #user_input = "\"House of cards best serie\""
    #print(r.get_posting(user_input))
    #print(r.get_posting(user_input))
    results = r.query(user_input)
    for doc_id in results:
        print("{}".format(doc_id))

    docnames_ids = r.get_docnames_ids()

    ## DELETE THIS
    for doc_id in results:
        print("{}".format(docnames_ids[doc_id]))


mostrar_menu_configuracion()
