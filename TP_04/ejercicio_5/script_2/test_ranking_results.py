BASEPATH = "/home/agustin/Desktop/Recuperacion/colecciones/collection_test/"

REINDEX = False

## Terrier SETUP
import pyterrier as pt
pt.init()

if REINDEX:
    files = pt.io.find_files(BASEPATH+"TestCollection/")
    indexer = pt.FilesIndexer(BASEPATH+"index", verbose=True, blocks=False)
    indexer.setProperty("tokeniser", "UTFTokeniser")
    indexer.setProperty("termpipelines", "SpanishSnowballStemmer")
    indexref = indexer.index(files)
    index = pt.IndexFactory.of(indexref)
else:
    indexref = pt.IndexRef.of(BASEPATH+"index/data.properties")
    
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

print('Ingrese la query')
user_input = input()

results = pt.BatchRetrieve(indexref, wmodel="TF_IDF", metadata=["docno", "filename"]).search(user_input)
terrier_results = {}
for row in results.iterrows():
    doc_id = int(row[1].filename.split("doc")[1].split(".txt")[0])
    terrier_results[doc_id] = row[1].score

my_results = r.query(user_input)

print(list(terrier_results.keys()))
print(list(my_results.keys()))

from scipy import stats
print(stats.spearmanr(list(terrier_results.keys()), list(my_results.keys())))
#print(list(terrier_results.keys())[:10])
#print(list(my_results.keys())[:10])






#topics = pt.io.read_topics(BASEPATH+"query-text.trec")
#qrels = pt.io.read_qrels(BASEPATH+"qrels")

#res = tf.transform(topics)
#print(res)

#pt.Utils.evaluate(res, qrels, metrics = ['map'])
