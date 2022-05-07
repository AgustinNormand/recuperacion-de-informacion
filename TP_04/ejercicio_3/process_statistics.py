import json
statistics = {}
with open('statistics.json', 'r') as fp:
    statistics = json.load(fp)


#import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np

disk_average_times = {}
mem_average_times = {}
for value in statistics:
    disk_average_times[value] = statistics[value]["disk_execution_time"]
    mem_average_times[value] = statistics[value]["mem_execution_time"]

disk_average_times = dict(sorted(disk_average_times.items(), key=lambda item: item[1]))
mem_average_times = dict(sorted(mem_average_times.items(), key=lambda item: item[1]))

plt.figure(0, figsize=(13, 7))
plt.plot(disk_average_times.keys(), disk_average_times.values())
plt.plot(mem_average_times.keys(), mem_average_times.values())
plt.xlabel("Tipo de consultas")
plt.ylabel("Tiempo de respuesta promedio")
plt.legend(['Disk Retrieval', "Memory Retrieval"])
plt.savefig("average_times")


acum = 0
counter = 0
for value in statistics:
    disk_execution_time_values = []
    mem_execution_time_values = []
    for query in statistics[value]["querys"]:
        disk_execution_time_values.append(query["disk_execution_time"])
        mem_execution_time_values.append(query["mem_execution_time"])
    acum += np.corrcoef(disk_execution_time_values, mem_execution_time_values)[0][1]
    counter += 1
print("Average correlation coeficient: {}".format(acum/counter))

##  

figure_number = 1
acum = 0
counter = 0
for value in statistics:
    mem_execution_time_values = {}
    for query in statistics[value]["querys"]:
        mem_execution_time_values[round(query["mem_execution_time"], 5)] = sum(query["postings_sizes"])/len(query["postings_sizes"])

    mem_execution_time_values = dict(sorted(mem_execution_time_values.items(), key=lambda item: item[1]))

    plt.figure(figure_number, figsize=(13, 7))
    figure_number += 1
    plt.plot(mem_execution_time_values.keys(), mem_execution_time_values.values())
    plt.xlabel("Tiempo de respuesta")
    plt.ylabel("Tamaño de las postings")
    plt.savefig(value)

    acum += np.corrcoef(list(mem_execution_time_values.keys()), list(mem_execution_time_values.values()))[0][1]
    counter += 1
print("Average correlation coeficient: {}".format(acum/counter))