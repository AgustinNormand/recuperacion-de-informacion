EMPTY_WORDS_PATH = "palabrasvacias.txt"
# "palabrasvacias.txt"
# "emptywords.txt"

DIRPATH = "/home/agustin/Desktop/Recuperacion/colecciones/collection_test_ER2/TestCollection/"
# "/home/agustin/Desktop/Recuperacion/colecciones/RI-tknz-data/"
# "/home/agustin/Desktop/Recuperacion/colecciones/wiki-small/"
# "/home/agustin/Desktop/Recuperacion/colecciones/wiki-txt/"
# "/home/agustin/Desktop/Recuperacion/colecciones/collection_test/TestCollection/"
# "/home/agustin/Desktop/Recuperacion/colecciones/collection_test_ER2/TestCollection/"

#Size of strings for Exporter to write binary file
#Posible: ["STATIC", "MAX", "AVERAGE"]
#STRING_SIZE_CRITERION = "STATIC" #TODO
#Static use DOCNAMES_SIZE and TERMS_SIZE
#MAX AND AVERAGE HAS TO REPLACE THIS VALUES! Need .env?

#Tokenizer term size
MIN_TERM_LENGTH = 3
MAX_TERM_LENGTH = 25
#

DOCNAMES_SIZE = 92
# RI-tknz-data = 115
# Wiki-Small = 172
# Wiki-txt = 1561
# Collection-Test = 89
# Collection-Test-ER2 = 92

TERMS_SIZE = 96
# Collection-Test-ER2 = 96
#

# None in order to not aplicate stemming
STEMMING_LANGUAGE = "spanish"
# english
# spanish
 
#Evaluate RE or not (Email, Abbreviations, Dates, ...)
EXTRACT_ENTITIES = True
#

#For wiki-small. Not consider HTML tags
HTML_FILES = False
#

# Only for Wiki-txt
CORPUS_FILES_ENCODING = "UTF-8"
# "ISO-8859-1"
# "UTF-8"

# Only for test_results.py
RESULTS_FILE = "/home/agustin/Desktop/Recuperacion/colecciones/collection_test_ER2/collection_data.json"
# "/home/agustin/Desktop/Recuperacion/colecciones/collection_test/collection_data.json"
# "/home/agustin/Desktop/Recuperacion/colecciones/collection_test_ER2/collection_data.json"
#

# True if doc_id is in doc_name. Example doc120.txt
ID_IN_DOCNAME = True
#

WORKERS_NUMBER = 10

#FIXME ABSOLUTE PATHS

INDEX_FILES_PATH = "/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/index_files/"

DOCNAMES_IDS_FILENAME = "docnames_ids"
VOCABULARY_FILENAME = "vocabulary"
INVERTED_INDEX_FILENAME = "inverted_index"
BIN_VOCABULARY_FILENAME = VOCABULARY_FILENAME+".bin"
TXT_VOCABULARY_FILENAME = VOCABULARY_FILENAME+".txt"
BIN_INVERTED_INDEX_FILENAME = INVERTED_INDEX_FILENAME+".bin"
TXT_INVERTED_INDEX_FILENAME = INVERTED_INDEX_FILENAME+".txt"
BIN_DOCNAMES_IDS_FILENAME = DOCNAMES_IDS_FILENAME+".bin"
TXT_DOCNAMES_IDS_FILENAME = DOCNAMES_IDS_FILENAME+".txt"

HUMAN_FILES_PATH = "/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/human_files/"

OVERHEAD_PLOT_PATH = "/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/human_files/overhead.png"
POSTINGS_PLOT_PATH = '/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/human_files/postings_distribution.png'
TITLE_LENGTH_PLOT_PATH = '/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/human_files/title_length.png'
TERM_LENGTH_PLOT_PATH = '/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/human_files/term_length.png'




