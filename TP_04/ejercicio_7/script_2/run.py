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
    import time
    metadata = {}
    with open(METADATA_FILE, 'r') as fp:
        metadata = json.load(fp)
    r = Retrieval(metadata, False, True)


    print('Ingrese el término para obtener la skip-list')
    user_input = input()
    results = r.get_skip(user_input)
    for result in results:
        #print("{} {}".format(result[0], result[1]))
        print("{}".format(result[0]))



mostrar_menu_configuracion()


