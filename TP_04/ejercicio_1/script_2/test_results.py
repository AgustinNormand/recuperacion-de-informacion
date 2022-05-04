# SET ID_IN_DOCNAME = True

import json

from retrieval import Retrieval

import sys
sys.path.append('../script_1')
from constants import *

r = Retrieval()

with open(RESULTS_FILE, "r") as f:
    data = json.load(f)
    print(data.keys())
    print("Data: {}".format(data["statistics"]))
    print("\r")

    
    vocabulary = []
    for value in data["data"]:
        vocabulary.append(value["term"])

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
            #print(len(value["term"]))
            print(collection_doc_ids)
            print(my_doc_ids)
            errors = True
            print("Error in term: {}".format(value["term"]))
            sys.exit()

    if not errors:
        print("All posting lists are equal")
    
 