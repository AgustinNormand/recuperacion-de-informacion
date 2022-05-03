## python3 menu.py ../../../../colecciones/collection_test_ER2/TestCollection/ palabrasvacias.txt spanish true true false
## python3 test_results.py ../../../../colecciones/collection_test_ER2/collection_data.json
import json
import sys

from retrieval import Retrieval

if len(sys.argv) > 1:
    dirpath = sys.argv[1]

r = Retrieval()

with open(dirpath, "r") as f:
    data = json.load(f)
    print(data.keys())
    print("Data: {}".format(data["statistics"]))
    print("\r")

    
    vocabulary = []
    for value in data["data"]:
        vocabulary.append(value["term"])
        #print("Term: {}".format(value["term"]))
        #print("Docids: {}".format(value["docid"]))
        #print("Freqs: {}".format(value["freq"]))
        #print("Df: {}".format(value["df"]))
        #break
    print("Collection vocabulary")
    print(vocabulary)
    print("\r")

    my_vocabulary = r.get_vocabulary()

    print("My vocabulary")
    print(my_vocabulary)
    print("\r")

    if len(vocabulary) == len(my_vocabulary):
        print("Same number of terms")
    else:
        print("Different number of terms")

    print("\r")

    errors = False
    for value in data["data"]:
        collection_doc_ids = value["docid"]
        my_doc_ids = r.get_posting(value["term"])
        if my_doc_ids != collection_doc_ids:
            print(len(value["term"]))
            print(my_doc_ids)
            errors = True
            print("Error in term: {}".format(value["term"]))
            #print(my_doc_ids)
#        else:
 #           print("Equal posting for term: {}".format(value["term"]))

    if not errors:
        print("All posting lists are equal")

        #print("Term: {}".format(value["term"]))
        #print("Docids: {}".format(value["docid"]))
        #print("Freqs: {}".format(value["freq"]))
        #print("Df: {}".format(value["df"]))
        #break
    
 