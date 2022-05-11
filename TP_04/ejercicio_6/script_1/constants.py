EMPTY_WORDS_PATH = "./palabrasvacias.txt"
# "palabrasvacias.txt"
# "emptywords.txt"
# None

DIRPATH = "/home/agustin/Desktop/Recuperacion/colecciones/testy_collection/"
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

EXTRACT_ENTITIES = False

CORPUS_FILES_ENCODING = "UTF-8"
# Wiki-Txt = "ISO-8859-1"
# All = "UTF-8"

ID_IN_DOCNAME = False

WORKERS_NUMBER = 10

INDEX_FILES_PATH = "./index_files/"

METADATA_FILE = INDEX_FILES_PATH+"metadata.json"

BIN_VOCABULARY_FILEPATH = INDEX_FILES_PATH+"vocabulary.bin"
BIN_INVERTED_INDEX_FILEPATH = INDEX_FILES_PATH+"inverted_index.bin"
BIN_DOCNAMES_IDS_FILEPATH = INDEX_FILES_PATH+"docnames_ids.bin"
BIN_NORM_FILEPATH = INDEX_FILES_PATH+"ids_norm.bin"
BIN_POSITIONS_FILEPATH = INDEX_FILES_PATH+"positions.bin"
