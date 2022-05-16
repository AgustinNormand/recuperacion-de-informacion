import sys
#sys.path.append('../ejercicio_1/script_1')
from retrieval import Retrieval
from constants import *
import json

def mostrar_menu_configuracion():
    print("Archivo de metadata: {}".format(METADATA_FILE))
    print("\r\n")
    mostrar_menu_principal()

def mostrar_menu_principal():
    metadata = {}
    with open(METADATA_FILE, 'r') as fp:
        metadata = json.load(fp)
    r = Retrieval(metadata, False)

    print('Ingrese la query')
    user_input = input()

    import time
    start = time.time()
    results = r.query(user_input)
    end = time.time()
    print(end - start)
   
    for document_id in results:
        print(document_id)

mostrar_menu_configuracion()


