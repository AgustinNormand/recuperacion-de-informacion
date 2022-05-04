import sys

from retrieval import Retrieval

empty_words_path = None

stemming_language = "spanish"
extract_entities = True

def strtobool(string):
    string = string.lower()
    if string == "true" or string == "yes" or string == "1" or string == "si":
        return True
    return False

if len(sys.argv) > 1:
    extract_entities = strtobool(sys.argv[1])

if len(sys.argv) > 2:
    stemming_language = sys.argv[2].lower()

#if len(sys.argv) > 1:
   # empty_words_path = sys.argv[1]

def mostrar_menu_configuracion():
    #print("python3 menu.py <path archivo palabras vacias>\r\n")
    print("python3 menu.py <extract_entities> <stemming_language> \r\n")
    print("Verifique los parámetros. \r\n")
    print("Stemming Language: {}".format(stemming_language))
    print("Extract Entities: {}".format(extract_entities))
    #print("Path del archivo de palabras vacias: {}".format(empty_words_path))
    print("\r\n")
    mostrar_menu_principal()

def mostrar_menu_principal():
    r = Retrieval()

    print('Ingrese la query')
    user_input = input()
    print(r.query(user_input))
    #posting_list = r.get_posting(user_input)
    #for posting in posting_list:
        #print(posting)

mostrar_menu_configuracion()
