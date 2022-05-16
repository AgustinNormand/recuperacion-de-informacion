import json
statistics = {}
with open('statistics.json', 'r') as fp:
    statistics = json.load(fp)

from constants import *
import matplotlib.pyplot as plt
import numpy as np

print("K_SKIPS: {}".format(K_SKIPS))

for value in statistics:
    print(value)
    print("{}: {}".format("Without Skips", statistics[value]["without_skips_execution_time"]))
    print("{}: {}".format("With Skips", statistics[value]["skips_execution_time"]))
    print("\r")

for value in statistics:
    for query in statistics[value]["querys"]:
        query["postings_sizes"] = min(query["postings_sizes"])



for value in statistics:
    keys = []
    without_skips = []
    with_skips = []
    sorted_querys = sorted(statistics[value]["querys"], key=lambda d: d['postings_sizes'])
    for query in sorted_querys: 
        keys.append(query["postings_sizes"])
        without_skips.append(query["without_skips_execution_time"])
        with_skips.append(query["skips_execution_time"])
        #print(query)
    plt.figure(0)
    plt.plot(keys, without_skips)
    plt.plot(keys, with_skips)
    plt.show()

#print(keys)
#plt.figure(0, figsize=(13, 7))

#plt.xlabel("Tipo de consultas")
#plt.ylabel("Tiempo de respuesta promedio")
#plt.legend(['Disk Retrieval', "Memory Retrieval"])
#plt.savefig("average_times")
