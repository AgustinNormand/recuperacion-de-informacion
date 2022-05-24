from constants import *
from TAAT_retrieval.taat_retrieval import *
from DAAT_retrieval.daat_retrieval import *
import json
import time
import sys

def measure_query_time(terms, retrieval):
    acum = 0
    counter = 0
    for i in range(3):
        start = time.time()
        retrieval.and_query(terms)
        end = time.time()
        counter += 1
        acum += end - start
    return acum / counter

def check_consistency(terms, retrieval1, retrieval2):
    result1 = retrieval1.and_query(terms)
    result2 = retrieval2.and_query(terms)
    if (result1 != result2):
        print(result1)
        print(result2)
        return False
    else:
        return True

metadata = {}
with open(INDEX_FILES_PATH+METADATA_FILE, 'r') as fp:
    metadata = json.load(fp)
    taat_r = TAAT_Retrieval(metadata)
    daat_r = DAAT_Retrieval(metadata)

#times_acumulator_taat = 0
#times_acumulator_daat = 0
#query_counter = 0


statistics = {}

query_types = [
    "{}_term_querys".format(1),
    "{}_term_querys".format(2),
    "{}_term_querys".format(3),
    "{}_term_querys".format(4),
    ]

for query_type in query_types:
    statistics[query_type] = {}
    statistics[query_type]["querys"] = []
    #statistics[query_type]["query_count"] = None
    #statistics[query_type]["average_time_taat"] = None
    #statistics[query_type]["average_time_daat"] = None

with open(QUERYS_FILE, "r") as f:
    for line in f.readlines():
        terms = line.strip().split(" ")

        query_statistics = {}
        query_statistics["query"] = terms
        postings_sizes = []
        for term in terms:
            postings_sizes.append(len(daat_r.get_posting(term)))
        query_statistics["postings_sizes"] = postings_sizes
        query_statistics["time_taat"] = measure_query_time(terms, taat_r)
        query_statistics["time_daat"] = measure_query_time(terms, daat_r)
        statistics["{}_term_querys".format(len(terms))]["querys"].append(query_statistics)

        if not check_consistency(terms, taat_r, daat_r):
            print("Diff results")
            sys.exit()

with open('statistics.json', 'w') as fp:
    json.dump(statistics, fp,  indent=4)

