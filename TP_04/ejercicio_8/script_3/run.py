from constants import *
from btree_retrieval.btree_retrieval import *
from skips_retrieval.skips_retrieval import *
from sets_retrieval.sets_retrieval import *
import json
import time
import sys

def measure_query_time(terms, retrieval):
    acum = 0
    counter = 0
    for i in range(5):
        start = time.time()
        retrieval.and_query(terms)
        end = time.time()
        counter += 1
        acum += end - start
    return acum / counter

def check_consistency(terms, retrieval1, retrieval2, retrieval3):
    result1 = retrieval1.and_query(terms)
    result2 = retrieval2.and_query(terms)
    result3 = retrieval3.and_query(terms)
    if (result1 != result2) or (result1 != result3) or (result2 != result3):
        print(result1)
        print(result2)
        print(result3)
        return False
    else:
        return True


metadata = {}
with open(INDEX_FILES_PATH+METADATA_FILE, 'r') as fp:
    metadata = json.load(fp)
    start = time.time()
    btree_r = Btree_Retrieval(metadata)
    end = time.time()
    print("Btree loadtime {}".format(end - start))

    start = time.time()
    skips_r = Skips_Retrieval(metadata)
    end = time.time()
    print("Skips loadtime {}".format(end - start))

    start = time.time()
    sets_r = Sets_Retrieval(metadata)
    end = time.time()
    print("Sets loadtime {}".format(end - start))


times_acumulator_btree = 0
times_acumulator_skips = 0
times_acumulator_sets = 0
query_counter = 0
for term_i in btree_r.get_vocabulary():
    for term_j in btree_r.get_vocabulary():
        if term_i == term_j:
            continue
        if not check_consistency([term_i, term_j], btree_r, skips_r, sets_r):
            print("Diff results")
            sys.exit()
        times_acumulator_btree += measure_query_time([term_i, term_j], btree_r)
        times_acumulator_skips += measure_query_time([term_i, term_j], skips_r)
        times_acumulator_sets += measure_query_time([term_i, term_j], sets_r)
        query_counter+= 1
        print("Quert counter {}, BTree {}, Skips {}, Sets {}".format(query_counter, times_acumulator_btree/query_counter, times_acumulator_skips/query_counter, times_acumulator_sets/query_counter))
