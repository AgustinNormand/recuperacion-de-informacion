# RESULTS_FILE = "/home/agustin/Desktop/Recuperacion/colecciones/collection_test_ER2/collection_data.json"
RESULTS_FILE = "/home/agustin/Desktop/Recuperacion/colecciones/collection_test/collection_data.json"

## TEST FOR POSTINGS AND DF

from constants import *

import json

from retrieval import Retrieval

metadata = {}
with open(METADATA_FILE, "r") as fp:
    metadata = json.load(fp)

import sys

r = Retrieval(metadata)


def extraer_doc_ids(postings_lists):
    result = []
    for posting_list in postings_lists:
        #print(posting_list)
        partial_result = [posting_list[0], posting_list[1]]
        #for posting in posting_list:
            #partial_result.append(posting[0])
        result.append(partial_result)
    return result


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
        frequency = value["freq"]
        df = r.get_vocabulary_value(value["term"])[0]
        if df != value["df"]:
            print("Different DF in term: {}".format(value["term"]))

        postings_lists = []
        for zip_value in zip(collection_doc_ids, frequency):
            postings_lists.append(list(zip_value))
        my_doc_ids = r.get_posting(value["term"])
        if extraer_doc_ids(my_doc_ids) != postings_lists:
            print(postings_lists)
            print(extraer_doc_ids(my_doc_ids))
            errors = True
            print("Error in term: {}".format(value["term"]))
            sys.exit()
        print("{} OK.".format(value["term"]))

    if not errors:
        print("All posting lists are equal")
