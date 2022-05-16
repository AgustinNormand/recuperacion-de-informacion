from constants import *
from importer import *

import json
import sys

def mostrar_menu_configuracion():
    print("Archivo de metadata: {}".format(INDEX_FILES_PATH+METADATA_FILE))
    print("\r\n")
    mostrar_menu_principal()

def mostrar_menu_principal():
    metadata = {}
    with open(INDEX_FILES_PATH+METADATA_FILE, 'r') as fp:
        metadata = json.load(fp)
    importer = Importer(metadata["TERMS_SIZE"])
    vocabulary = importer.read_vocabulary()

    print(vocabulary["alejandro"])

    print("1) DGAPS")
    print("2) SKIPS")
    print("3) POSTINGS")
    user_input_option = int(input())
    print('Ingrese el término')

    user_input_term = input()

    try:
        df, index_pointer, skips_pointer, dgaps_pointer = vocabulary[user_input_term]
    except:
        sys.exit()

    if user_input_option == 1:
        dgaps = importer.get_dgaps_part(dgaps_pointer, df)
        for value in dgaps:
            print(value)

    if user_input_option == 2:
        skips = importer.get_skips_part(dgaps_pointer, df)
        for value in skips:
            print(value[0])

    if user_input_option == 3:
        posting = importer.get_posting_part(dgaps_pointer, df)
        #print(posting)
        for value in posting:
            print(value)




    #posting_list = r.get_posting(user_input)
    #for posting in posting_list:
    #    print(posting)

mostrar_menu_configuracion()
