#RESULTS_FILE = "/home/agustin/Desktop/Recuperacion/colecciones/collection_test_ER2/collection_data.json"
RESULTS_FILE = "/home/agustin/Desktop/Recuperacion/colecciones/collection_test/collection_data.json"


import json
from retrieval import Retrieval

import sys
#sys.path.append('../ejercicio_1/script_1')
from constants import *

metadata = {}
with open(METADATA_FILE, 'r') as fp:
    metadata = json.load(fp)

r = Retrieval(metadata)

with open(RESULTS_FILE, "r") as f:
    data = json.load(f)
    print(data.keys())
    print("Data: {}".format(data["statistics"]))
    print("\r")

    
    vocabulary = {}
    for value in data["data"]:
        vocabulary[value["term"]] = value["docid"]
    print("Collection vocabulary")
    print(vocabulary.keys())
    print("\r")

    print("My vocabulary")
    print(r.get_vocabulary())

    

    querys = 0

    for key_i in vocabulary:
        for key_j in vocabulary:
            for symbol in [AND_SYMBOL, OR_SYMBOL, NOT_SYMBOL]:
                if key_i == key_j:
                    continue
                query = "{}{}{}".format(key_i, symbol, key_j)
                my_resultset = r.query(query)
                querys += 1

                if symbol == AND_SYMBOL:
                    result_set = sorted(list(set(vocabulary[key_i]).intersection(set(vocabulary[key_j]))))
                if symbol == OR_SYMBOL:
                    result_set = sorted(list(set(vocabulary[key_i]).union(set(vocabulary[key_j]))))
                if symbol == NOT_SYMBOL:
                    result_set = sorted(list(set(vocabulary[key_i]).difference(set(vocabulary[key_j]))))
                if not result_set == my_resultset:
                    print("Diferent resultset in {}".format(query))
                    print(my_resultset)
                    print(result_set)
                    sys.exit()

    for key_i in vocabulary:
        for key_j in vocabulary:
            for key_k in vocabulary:
                if key_i == key_j or key_i == key_k or key_j == key_k:
                    continue
                query = "{}{}{}{}{}".format(key_i, AND_SYMBOL, key_j, AND_SYMBOL, key_k)
                result_set = sorted(list(set(vocabulary[key_i]).intersection(set(vocabulary[key_j])).intersection(set(vocabulary[key_k]))))
                my_resultset = r.query(query)
                querys += 1
                if not result_set == my_resultset:
                    errors = True
                    print("Diferent resultset in {}".format(query))
                    print(my_resultset)
                    print(result_set)
                    sys.exit()
                
                query = "({}{}{}){}{}".format(key_i, AND_SYMBOL, key_j, NOT_SYMBOL, key_k)
                result_set = set(vocabulary[key_i]).intersection(set(vocabulary[key_j]))
                result_set = result_set.difference(set(vocabulary[key_k]))
                result_set = sorted(list(result_set))
                my_resultset = r.query(query)
                querys += 1
                if not result_set == my_resultset:
                    errors = True
                    print("Diferent resultset in {}".format(query))
                    print(my_resultset)
                    print(result_set)
                    sys.exit()
                
                query = "({}{}{}){}{}".format(key_i, AND_SYMBOL, key_j, OR_SYMBOL, key_k)
                result_set = set(vocabulary[key_i]).intersection(set(vocabulary[key_j]))
                result_set = result_set.union(set(vocabulary[key_k]))
                result_set = sorted(list(result_set))
                my_resultset = r.query(query)
                querys += 1
                if not result_set == my_resultset:
                    errors = True
                    print("Diferent resultset in {}".format(query))
                    print(my_resultset)
                    print(result_set)
                    sys.exit()
                
                query = "({}{}{}){}{}".format(key_i, OR_SYMBOL, key_j, AND_SYMBOL, key_k)
                result_set = set(vocabulary[key_i]).union(set(vocabulary[key_j]))
                result_set = result_set.intersection(set(vocabulary[key_k]))
                result_set = sorted(list(result_set))
                my_resultset = r.query(query)
                querys += 1
                if not result_set == my_resultset:
                    errors = True
                    print("Diferent resultset in {}".format(query))
                    print(my_resultset)
                    print(result_set)
                    sys.exit()
                
                query = "({}{}{}){}{}".format(key_i, OR_SYMBOL, key_j, NOT_SYMBOL, key_k)
                result_set = set(vocabulary[key_i]).union(set(vocabulary[key_j]))
                result_set = result_set.difference(set(vocabulary[key_k]))
                result_set = sorted(list(result_set))
                my_resultset = r.query(query)
                querys += 1
                if not result_set == my_resultset:
                    errors = True
                    print("Diferent resultset in {}".format(query)) 
                    print(my_resultset)
                    print(result_set)
                    sys.exit()
                    
    print("Amount of querys done: {}".format(querys))