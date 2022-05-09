EMPTY_WORDS_PATH = "./emptywords.txt"
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

STRING_STORE_CRITERION = "MAX"
# MAX
# STATIC

# ONLY FOR STATIC STRING_STORE_CRITERION
DOCNAMES_SIZE = 50
TERMS_SIZE = 50


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

# True if doc_id is in doc_name. Example doc120.txt
ID_IN_DOCNAME = False

WORKERS_NUMBER = 10

INDEX_FILES_PATH = "./output/index_files/"

DOCNAMES_IDS_FILENAME = "docnames_ids"
VOCABULARY_FILENAME = "vocabulary"
INVERTED_INDEX_FILENAME = "inverted_index"
BIN_VOCABULARY_FILENAME = VOCABULARY_FILENAME+".bin"
TXT_VOCABULARY_FILENAME = VOCABULARY_FILENAME+".txt"
BIN_INVERTED_INDEX_FILENAME = INVERTED_INDEX_FILENAME+".bin"
TXT_INVERTED_INDEX_FILENAME = INVERTED_INDEX_FILENAME+".txt"
BIN_DOCNAMES_IDS_FILENAME = DOCNAMES_IDS_FILENAME+".bin"
TXT_DOCNAMES_IDS_FILENAME = DOCNAMES_IDS_FILENAME+".txt"

METADATA_FILE = "metadata.json"

PLOT_RESULTS = False

HUMAN_FILES_PATH = "./output/human_files/"

OVERHEAD_PLOT_PATH = "./output/human_files/overhead.png"
POSTINGS_PLOT_PATH = './output/human_files/postings_distribution.png'
TITLE_LENGTH_PLOT_PATH = './output/human_files/title_length.png'
TERM_LENGTH_PLOT_PATH = './output/human_files/term_length.png'