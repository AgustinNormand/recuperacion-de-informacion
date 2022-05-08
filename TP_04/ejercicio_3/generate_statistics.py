import sys
sys.path.append('../ejercicio_1/script_1')
from constants import *
sys.path.append('../ejercicio_2/')
from retrieval import *
import time

QUERYS_FILE_PATH = "/home/agustin/Desktop/Recuperacion/repo/TP_04/ejercicio_3/queries_2y3t.txt"



SYMBOLS = [AND_SYMBOL, OR_SYMBOL, NOT_SYMBOL]

r = Retrieval()

statistics = {}

query_types = [
    "two_term_{}_querys".format(AND_SYMBOL), 
    "two_term_{}_querys".format(OR_SYMBOL), 
    "two_term_{}_querys".format(NOT_SYMBOL), 
    "tree_term_querys_type_a", 
    "tree_term_querys_type_b", 
    "tree_term_querys_type_c"]

for query_type in query_types:
    statistics[query_type] = {}
    statistics[query_type]["querys"] = []
    statistics[query_type]["disk_execution_time"] = None
    statistics[query_type]["mem_execution_time"] = None
    statistics[query_type]["query_count"] = None

def build_two_term_querys(term0, term1):
    for symbol in SYMBOLS:
        query_statistics = {}
        query_statistics["query"] = "{}{}{}".format(term0, symbol, term1)
        query_statistics["postings_sizes"] = [len(r.get_posting(term0)), len(r.get_posting(term1))]
        query_statistics["disk_execution_time"] = None
        query_statistics["mem_execution_time"] = None
        statistics["two_term_{}_querys".format(symbol)]["querys"].append(query_statistics)


def build_tree_term_querys(term0, term1, term2):
    query_statistics = {}
    query_statistics["query"] = "{}{}{}{}{}".format(term0, AND_SYMBOL, term1, AND_SYMBOL, term2)
    query_statistics["postings_sizes"] = [len(r.get_posting(term0)), len(r.get_posting(term1)), len(r.get_posting(term2))]
    query_statistics["disk_execution_time"] = None
    query_statistics["mem_execution_time"] = None
    statistics["tree_term_querys_type_a"]["querys"].append(query_statistics)

    query_statistics = {}
    query_statistics["query"] = "({}{}{}){}{}".format(term0, OR_SYMBOL, term1, NOT_SYMBOL, term2)
    query_statistics["postings_sizes"] = [len(r.get_posting(term0)), len(r.get_posting(term1)), len(r.get_posting(term2))]
    query_statistics["disk_execution_time"] = None
    query_statistics["mem_execution_time"] = None
    statistics["tree_term_querys_type_b"]["querys"].append(query_statistics)

    query_statistics = {}
    query_statistics["query"] = "({}{}{}){}{}".format(term0, AND_SYMBOL, term1, OR_SYMBOL, term2)
    query_statistics["postings_sizes"] = [len(r.get_posting(term0)), len(r.get_posting(term1)), len(r.get_posting(term2))]
    query_statistics["disk_execution_time"] = None
    query_statistics["mem_execution_time"] = None
    statistics["tree_term_querys_type_c"]["querys"].append(query_statistics)

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

mem_retrieval = Retrieval(True)

for value in statistics:
    counter = 0
    disk_acumulator = 0
    mem_acumulator = 0
    for query in statistics[value]["querys"]:
        query_time = measure_query_time(query["query"], r)
        mem_query_time = measure_query_time(query["query"], mem_retrieval)

        if r.query(query["query"]) != mem_retrieval.query(query["query"]):
            print("Diff results")
            print(query["query"])
        counter += 1

        disk_acumulator += query_time
        mem_acumulator += mem_query_time

        query["disk_execution_time"] = query_time
        query["mem_execution_time"] = mem_query_time

    statistics[value]["disk_execution_time"] = disk_acumulator/counter
    statistics[value]["mem_execution_time"] = mem_acumulator/counter
    statistics[value]["query_count"] = counter

import json
with open('statistics.json', 'w') as fp:
    json.dump(statistics, fp,  indent=4)