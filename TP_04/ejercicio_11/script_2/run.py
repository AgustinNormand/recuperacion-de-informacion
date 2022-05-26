from constants import *
#from retrieval import *
from importer import *
import json
import time
import sys


CHECK_CONSISTENCY = True

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

        if CHECK_CONSISTENCY:
            for term in vocabulary:
                index_posting = i.read_posting(term, vocabulary, True)
                variable_posting = i.read_posting_variable(term, vocabulary, True)
                gamma_posting = i.read_posting_gamma(term, vocabulary, True)
                if gamma_posting != index_posting or variable_posting != index_posting or gamma_posting != variable_posting:
                    print("Error in: "+term)
                    #print(variable_posting)
                    #print(gamma_posting)
                    #print(index_posting)
                    sys.exit()

        start = time.time()
        for term in vocabulary:
            index_posting = i.read_posting(term, vocabulary, True)
        end = time.time()
        print("read_posting: {} seconds.".format(end - start))

        start = time.time()
        for term in vocabulary:
            variable_posting = i.read_posting_variable(term, vocabulary, True)
        end = time.time()
        print("read_posting_variable: {} seconds.".format(end - start))

        start = time.time()
        for term in vocabulary:
            gamma_posting = i.read_posting_gamma(term, vocabulary, True)
        end = time.time()
        print("read_posting_gamma: {} seconds.".format(end - start))



mostrar_menu_configuracion()
