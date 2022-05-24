import json
import numpy as np
import matplotlib.pyplot as plt


statistics = {}
with open('statistics.json', 'r') as fp:
    statistics = json.load(fp)

fig = 0
for query_type in statistics:
    values_taat = []
    values_daat = []
    postingsSizes_timeTAAT = {}
    postingsSizes_timeDAAT = {}
    for query in statistics[query_type]["querys"]:
        values_taat.append(query["time_taat"])
        values_daat.append(query["time_daat"])

        if min(query["postings_sizes"]) not in postingsSizes_timeTAAT.keys():
            postingsSizes_timeTAAT[min(query["postings_sizes"])] = [query["time_taat"]]
        else:
            postingsSizes_timeTAAT[min(query["postings_sizes"])].append(query["time_taat"])

        if min(query["postings_sizes"]) not in postingsSizes_timeDAAT.keys():
            postingsSizes_timeDAAT[min(query["postings_sizes"])] = [query["time_daat"]]
        else:
            postingsSizes_timeDAAT[min(query["postings_sizes"])].append(query["time_daat"])

    print("{}: Average_time_taat {}, Average_time_daat {}".format(query_type, sum(values_taat)/len(values_taat), sum(values_daat)/len(values_daat)))
    fig += 1
    plt.figure(fig)
    values = []
    keys = sorted(postingsSizes_timeTAAT.keys())
    for key in keys:
        values.append(sum(postingsSizes_timeTAAT[key])/len(postingsSizes_timeTAAT[key]))
    plt.plot(keys, values)

    values = []
    keys = sorted(postingsSizes_timeDAAT.keys())
    for key in keys:
        values.append(sum(postingsSizes_timeDAAT[key]) / len(postingsSizes_timeDAAT[key]))
    plt.plot(keys, values)

    plt.title(query_type)
    plt.xlabel("Tamaño de la posting mas chica")
    plt.ylabel("Tiempo de respuesta de la consulta")
    plt.legend(['TAAT', "DAAT"])

    for key in postingsSizes_timeTAAT.keys():
        if key > 100000:
            print(postingsSizes_timeTAAT[key])

    plt.show()