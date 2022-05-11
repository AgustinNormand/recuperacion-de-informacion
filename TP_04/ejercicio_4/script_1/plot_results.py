times = {}
times[76] = [271.8071989218394, 22.21466628710429]
times[151] = [272.64158058166504, 18.06307601928711]
times[302] = [271.07223471005756, 15.516569375991821]
times[604] = [274.42263730367023, 13.907117366790771]
times[1210] = [273.58787059783936, 12.69956644376119]
times[2420] = [275.2257897059123, 12.186079740524292]

import matplotlib.pyplot as plt

index_times = []
merge_times = []
for key in times:
    index_times.append(times[key][0])
    merge_times.append(times[key][1])

plt.figure(0)
plt.plot(times.keys(), index_times)
plt.xlabel("Limite de documentos")
plt.ylabel("Tiempo de indexación")
plt.savefig("./output/index")

plt.figure(1)
plt.plot(times.keys(), merge_times)
plt.xlabel("Limite de documentos")
plt.ylabel("Tiempo de merge")
plt.savefig("./output/merge")

print("Index range: {} {}".format(min(index_times), max(index_times)))
print("Merge range: {} {}".format(min(merge_times), max(merge_times)))

