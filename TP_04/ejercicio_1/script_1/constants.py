EMPTY_WORDS_PATH = "emptywords.txt"
# "palabrasvacias.txt"
# "emptywords.txt"
# None

DIRPATH = "/home/agustin/Desktop/Recuperacion/colecciones/wiki-txt/"
# "/home/agustin/Desktop/Recuperacion/colecciones/RI-tknz-data/"
# "/home/agustin/Desktop/Recuperacion/colecciones/wiki-small/"
# "/home/agustin/Desktop/Recuperacion/colecciones/wiki-txt/"
# "/home/agustin/Desktop/Recuperacion/colecciones/collection_test/TestCollection/"
# "/home/agustin/Desktop/Recuperacion/colecciones/collection_test_ER2/TestCollection/"

#Tokenizer term size
MIN_TERM_LENGTH = 3
MAX_TERM_LENGTH = 25
#

DOCNAMES_SIZE = 156
# Depends with the collection used
# RI-tknz-data = 115
# Wiki-Small = 172
# Wiki-txt = 156
# Collection-Test = 89
# Collection-Test-ER2 = 92

TERMS_SIZE = 80
# Depends with the collection used
# Collection-Test-ER2 = 96
# RI-tknz-data = ?
# Wiki-txt = 80?

STEMMING_LANGUAGE = "english"
# Depends with the collection used
# english
# spanish
# None
 
#Evaluate RE or not (Email, Abbreviations, Dates, ...)
EXTRACT_ENTITIES = True
#

#For wiki-small. Not consider HTML tags
HTML_FILES = False
#


CORPUS_FILES_ENCODING = "ISO-8859-1"
# Wiki-Txt = "ISO-8859-1"
# All = "UTF-8"

# Only for test_results.py
RESULTS_FILE = "/home/agustin/Desktop/Recuperacion/colecciones/collection_test_ER2/collection_data.json"
# "/home/agustin/Desktop/Recuperacion/colecciones/collection_test/collection_data.json"
# "/home/agustin/Desktop/Recuperacion/colecciones/collection_test_ER2/collection_data.json"

# True if doc_id is in doc_name. Example doc120.txt
ID_IN_DOCNAME = False
#

WORKERS_NUMBER = 10

AND_SYMBOL = "&"
OR_SYMBOL = "|"
NOT_SYMBOL = "-"

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

PLOT_RESULTS = False

HUMAN_FILES_PATH = "/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/human_files/"

OVERHEAD_PLOT_PATH = "/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/human_files/overhead.png"
POSTINGS_PLOT_PATH = '/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/human_files/postings_distribution.png'
TITLE_LENGTH_PLOT_PATH = '/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/human_files/title_length.png'
TERM_LENGTH_PLOT_PATH = '/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_1/script_1/output/human_files/term_length.png'

QUERYS_FILE_PATH = "/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_3/queries_2y3t.txt"




