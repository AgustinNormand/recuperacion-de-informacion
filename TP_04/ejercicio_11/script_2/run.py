from constants import *
#from retrieval import *
from importer import *
import json
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

        for term in vocabulary:
            variable_posting = i.read_posting_variable(term, vocabulary)
            gamma_posting = i.read_posting_gamma(term, vocabulary)
            index_posting = i.read_posting(term, vocabulary)
            if variable_posting != gamma_posting:
                print("Error in: "+term)
                print(variable_posting)
                print(gamma_posting)
                print(index_posting)
                break
            #else:
                #print("Ok "+term)

    #r = Retrieval(metadata)

    #print('Ingrese la query')
    #user_input = input()
    #results = r.query(user_input)
    #for doc_id in results:
#        print("{} {}".format(doc_id, results[doc_id]))

mostrar_menu_configuracion()
