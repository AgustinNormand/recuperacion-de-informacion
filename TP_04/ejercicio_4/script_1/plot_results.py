times = {}
times[76] = [276.0338673591614, 46.835002183914185]
times[151] = [327.7100336551666, 38.12986445426941]
times[302] = [387.84252977371216, 23.397321462631226]
times[604] = [325.9673557281494, 22.63266921043396]
times[1210] = [397.2900092601776, 15.86511754989624]
times[2420] = [363.08713603019714, 14.368023872375488]

import matplotlib.pyplot as plt

index_times = []
merge_times = []
for key in times:
    index_times.append(times[key][0])
    merge_times.append(times[key][1])

plt.figure(0)
plt.plot(times.keys(), index_times)
plt.show()

plt.figure(1)
plt.plot(times.keys(), merge_times)
plt.show()
#plt.xlabel("Overhead")
#plt.ylabel("Cantidad de documentos")

