
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

    if data["statistics"]["num_terms"] == len(r.get_vocabulary()):
        print("Same number of terms")
    else:
        print("Different number of terms")
    vocabulary = []
    for value in data["data"]:
        vocabulary.append(value["term"])
        #print("Term: {}".format(value["term"]))
        #print("Docids: {}".format(value["docid"]))
        #print("Freqs: {}".format(value["freq"]))
        #print("Df: {}".format(value["df"]))
        #break
    print(vocabulary)
    print("\r")


    for value in data["data"]:

        collection_doc_ids = value["docid"]
        
        my_doc_ids = r.get_posting(value["term"])
        errors = False
        if my_doc_ids != collection_doc_ids:
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
    
 