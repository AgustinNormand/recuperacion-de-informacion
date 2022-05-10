#import sys
#sys.path.append('../script_1')
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

    print('Ingrese el término del cual quiere la posting list')
    user_input = input()
    posting_list = r.get_posting(user_input)
    for posting in posting_list:
        print(posting)

mostrar_menu_configuracion()
