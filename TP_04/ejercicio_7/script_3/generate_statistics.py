from constants import *
import sys
sys.path.append('../script_2/')
from retrieval import *
import time
import json

metadata = {}
with open(METADATA_FILE, 'r') as fp:
    metadata = json.load(fp)

SYMBOLS = [AND_SYMBOL]

r = Retrieval(metadata, False, True, True)
skip_retrieval = Retrieval(metadata, False, True, False)

statistics = {}

query_types = [
    "two_term_{}_querys".format(AND_SYMBOL), 
    "tree_term_querys_type_a", 
    ]

for query_type in query_types:
    statistics[query_type] = {}
    statistics[query_type]["querys"] = []
    statistics[query_type]["query_count"] = None

def build_two_term_querys(term0, term1):
    for symbol in SYMBOLS:
        query_statistics = {}
        query_statistics["query"] = "{}{}{}".format(term0, symbol, term1)
        query_statistics["postings_sizes"] = [len(r.get_posting(term0)), len(r.get_posting(term1))]
        for value in query_statistics["postings_sizes"]:
            if value == 0:
                return
        statistics["two_term_{}_querys".format(symbol)]["querys"].append(query_statistics)


def build_tree_term_querys(term0, term1, term2):
    query_statistics = {}
    query_statistics["query"] = "{}{}{}{}{}".format(term0, AND_SYMBOL, term1, AND_SYMBOL, term2)
    query_statistics["postings_sizes"] = [len(r.get_posting(term0)), len(r.get_posting(term1)), len(r.get_posting(term2))]
    for value in query_statistics["postings_sizes"]:
        if value == 0:
            return
    statistics["tree_term_querys_type_a"]["querys"].append(query_statistics)

with open(QUERYS_FILE_PATH, "r") as f:
    for line in f.readlines():
        line = line.replace("\n", "")
        terms = line.split(" ")
        if len(terms) == 2:
            build_two_term_querys(terms[0], terms[1])
        else:
            if len(terms) == 3:
                build_tree_term_querys(terms[0], terms[1], terms[2])

def measure_query_time(query, retrieval):
    acum = 0
    counter = 0
    for i in range(10):
        start = time.time()
        retrieval.query(query)
        end = time.time()
        counter += 1
        acum += end - start
    return acum / counter

for value in statistics:
    counter = 0
    without_skips_acumulator = 0
    skip_acumulator = 0
    for query in statistics[value]["querys"]:
        without_skips_query_time = measure_query_time(query["query"], r)
        skips_query_time = measure_query_time(query["query"], skip_retrieval)
        if r.query(query["query"]) != skip_retrieval.query(query["query"]):
            print("Diff results")
            print(query["query"])

        counter += 1

        without_skips_acumulator += without_skips_query_time
        skip_acumulator += skips_query_time

        query["without_skips_execution_time"] = without_skips_query_time
        query["skips_execution_time"] = skips_query_time

    statistics[value]["without_skips_execution_time"] = without_skips_acumulator/counter
    statistics[value]["skips_execution_time"] = skip_acumulator/counter
    statistics[value]["query_count"] = counter


with open('statistics.json', 'w') as fp:
    json.dump(statistics, fp,  indent=4)