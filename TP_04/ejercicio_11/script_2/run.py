from constants import *
#from retrieval import *
from importer import *
import json
import time
import sys


def mostrar_menu_configuracion():
    print("Archivo de metadata: {}".format(METADATA_FILE))
    print("\r\n")
    mostrar_menu_principal()

def mostrar_menu_principal():
    metadata = {}
    with open(METADATA_FILE, 'r') as fp:
        metadata = json.load(fp)
        i = Importer(metadata["TERMS_SIZE"])
        vocabulary = i.read_vocabulary()

        start = time.time()
        for term in vocabulary:
            index_posting = i.read_posting(term, vocabulary)
            break
        end = time.time()
        print("read_posting: {} seconds.".format(end - start))

        start = time.time()
        for term in vocabulary:
            variable_posting = i.read_posting_variable(term, vocabulary)
        end = time.time()
        print("read_posting_variable: {} seconds.".format(end - start))

        start = time.time()
        for term in vocabulary:
            gamma_posting = i.read_posting_gamma(term, vocabulary)
        end = time.time()
        print("read_posting_gamma: {} seconds.".format(end - start))

            #if gamma_posting != index_posting or variable_posting != index_posting or gamma_posting != variable_posting:
                #print("Error in: "+term)
                #print(variable_posting)
                #print(gamma_posting)
                #print(index_posting)
                #break

mostrar_menu_configuracion()
