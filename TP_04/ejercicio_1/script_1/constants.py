EMPTY_WORDS_PATH = "./palabrasvacias.txt"
# "palabrasvacias.txt"
# "emptywords.txt"
# None

DIRPATH = "/home/agustin/Desktop/Recuperacion/colecciones/RI-tknz-data/"
# "/home/agustin/Desktop/Recuperacion/colecciones/RI-tknz-data/"
# "/home/agustin/Desktop/Recuperacion/colecciones/wiki-small/"
# "/home/agustin/Desktop/Recuperacion/colecciones/wiki-txt/"
# "/home/agustin/Desktop/Recuperacion/colecciones/collection_test/TestCollection/"
# "/home/agustin/Desktop/Recuperacion/colecciones/collection_test_ER2/TestCollection/"

MIN_TERM_LENGTH = 3
MAX_TERM_LENGTH = 25

STRING_STORE_CRITERION = "MAX"
# MAX
# STATIC

DOCNAMES_SIZE = 50
TERMS_SIZE = 50

STEMMING_LANGUAGE = "spanish"
# english
# spanish
# None

EXTRACT_ENTITIES = False
# True
# False

HTML_FILES = False
# True
# False

CORPUS_FILES_ENCODING = "UTF-8"
# Wiki-Txt = "ISO-8859-1"
# All = "UTF-8"

ID_IN_DOCNAME = False
# True
# False

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
# True
# False

COMPUTE_OVERHEAD = False
# True
# False

HUMAN_FILES_PATH = "./output/human_files/"

OVERHEAD_PLOT_PATH = "./output/human_files/overhead.png"
POSTINGS_PLOT_PATH = './output/human_files/postings_distribution.png'
TITLE_LENGTH_PLOT_PATH = './output/human_files/title_length.png'
TERM_LENGTH_PLOT_PATH = './output/human_files/term_length.png'