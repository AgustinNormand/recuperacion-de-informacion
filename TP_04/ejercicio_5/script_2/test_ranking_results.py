DIRPATH = "/home/agustin/Desktop/Recuperacion/colecciones/wiki-txt/"

INDEX_PATH = "/home/agustin/Desktop/Recuperacion/colecciones/Terrier_Index/"

REINDEX = True

INTERACTIVE = False

ENGLISH = True

from scipy import stats

## Terrier SETUP
import pyterrier as pt
pt.init()

if REINDEX:
    files = pt.io.find_files(DIRPATH)
    indexer = pt.FilesIndexer(INDEX_PATH, verbose=True, blocks=False)
    if not ENGLISH:
        indexer.setProperty("tokeniser", "UTFTokeniser")
        indexer.setProperty("termpipelines", "SpanishSnowballStemmer")
    indexref = indexer.index(files)
    index = pt.IndexFactory.of(indexref)
else:
    indexref = pt.IndexRef.of(INDEX_PATH+"data.properties")
    
##

## MY SETUP
from constants import *
from retrieval import *
import json
metadata = {}
with open(METADATA_FILE, 'r') as fp:
    metadata = json.load(fp)
    r = Retrieval(metadata)
##

def query(user_input):
    results = pt.BatchRetrieve(indexref, wmodel="TF_IDF", metadata=["docno", "filename"]).search(user_input)
    terrier_results = {}
    for row in results.iterrows():
        doc_id = int(row[1].filename.split("doc")[1].split(".txt")[0])
        terrier_results[doc_id] = row[1].score

    terrier_results = list(terrier_results.keys())
    my_results = list(r.query(user_input).keys())

    min_length = min([len(terrier_results), len(my_results)])
    return stats.spearmanr(terrier_results[:min_length], my_results[:min_length])

if INTERACTIVE:
    print('Ingrese la query')
    user_input = input()
    print("Correlation: {}".format(query(user_input).correlation))

else:
    
    vocabulary = list(r.get_vocabulary())

    two_term_querys = []
    for term_i in vocabulary:
        for term_j in vocabulary:
            if term_i == term_j:
                continue
            two_term_querys.append("{} {}".format(term_i, term_j))

    correlation_acum = 0
    counter = 0
    for two_term_query in two_term_querys:
        correlation_acum += query(two_term_query).correlation
        counter += 1
    print("Average correlation two term querys: {}".format(correlation_acum/counter))