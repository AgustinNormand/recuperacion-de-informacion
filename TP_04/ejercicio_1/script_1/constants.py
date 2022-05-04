EMPTY_WORDS_PATH = "palabrasvacias.txt"
DIRPATH = "/home/agustin/Desktop/Recuperacion/colecciones/collection_test_ER2/TestCollection/"

OVERHEAD_PLOT_PATH = "/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/human_files/overhead.png"
POSTINGS_PLOT_PATH = '/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/human_files/postings_distribution.png'

INDEX_FILES_PATH = "/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/index_files/"
HUMAN_FILES_PATH = "/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/human_files/"

#FIXME ABSOLUTE PATHS

#Size of strings for Exporter to write binary file
DOCNAMES_SIZE = 115
TERMS_SIZE = 100
#

#Tokenizer term size
MIN_TERM_LENGTH = 3
MAX_TERM_LENGTH = 25
#

STEMMING_LANGUAGE = "spanish"

#Evaluate RE or not (Email, Abbreviations, Dates, ...)
EXTRACT_ENTITIES = True
#

#For wiki-small. Not consider HTML tags
HTML_FILES = False
#

DOCNAMES_IDS_FILENAME = "docnames_ids"
VOCABULARY_FILENAME = "vocabulary"
INVERTED_INDEX_FILENAME = "inverted_index"

BIN_VOCABULARY_FILENAME = VOCABULARY_FILENAME+".bin"
TXT_VOCABULARY_FILENAME = VOCABULARY_FILENAME+".txt"

BIN_INVERTED_INDEX_FILENAME = INVERTED_INDEX_FILENAME+".bin"
TXT_INVERTED_INDEX_FILENAME = INVERTED_INDEX_FILENAME+".txt"

BIN_DOCNAMES_IDS_FILENAME = DOCNAMES_IDS_FILENAME+".bin"
TXT_DOCNAMES_IDS_FILENAME = DOCNAMES_IDS_FILENAME+".txt"

# Only for test_results.py
RESULTS_FILE = "/home/agustin/Desktop/Recuperacion/colecciones/collection_test_ER2/collection_data.json"
ID_IN_DOCNAME = True
#