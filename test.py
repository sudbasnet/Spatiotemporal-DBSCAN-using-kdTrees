import fileinput
from haversine import haversine
from datetime import datetime, timedelta
import time


def prep(file):
    points = []
    for line in fileinput.input(file):
        info = line.split(',')
        points.append((int(info[0]), float(info[1]), float(info[2]), int(info[3])))
        # print((int(info[0]), float(info[1]), float(info[2]), int(info[3])))
    return points


events2 = {}
d2 = (100, 30)
delta_t2 = timedelta(days=d2[1])
delta_s2 = d2[0]
dataset2 = prep('events_data_write.csv')
start = time.time()
for i in dataset2:
    nn_array = []
    for j in dataset2:
        if haversine((i[1], i[2]), (j[1], j[2])) <= delta_s2 and datetime.strptime(str(i[3]), '%Y%m%d') - datetime.strptime(str(j[3]), '%Y%m%d') <= delta_t2:
            nn_array.append(j[0])
    events2.update({i[0]: nn_array})


end = time.time()
print(end - start)

# 446.3999857902527