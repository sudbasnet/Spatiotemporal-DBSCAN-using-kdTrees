import fileinput
from haversine import haversine
from datetime import datetime, timedelta
import time
from spatialkdtree import Node, generate, Node, fixed_radius_neighbors, get_bbox


# this script uses brute force technique
def prep(file):
    points = []
    for line in fileinput.input(file):
        info = line.split(',')
        points.append((int(info[0]), float(info[1]), float(info[2]), int(info[3])))
        # print((int(info[0]), float(info[1]), float(info[2]), int(info[3])))
    return points


events2 = {}
d2 = (50, 30)
delta_t2 = timedelta(days=d2[1])
delta_s2 = d2[0]
dataset2 = prep('query_result.csv')


def getnode(dd, ids):
    for d in dd:
        if d[0]==ids:
            print(d)


start = time.time()
for i in dataset2:
    nn_array = []
    for j in dataset2:
        if haversine((i[2], i[1]), (j[2], j[1])) <= delta_s2 and abs(datetime.strptime(str(i[3]), '%Y%m%d') -
                                                                     datetime.strptime(str(j[3]), '%Y%m%d')) <= delta_t2 \
                and i[0] != j[0]:
            nn_array.append(j[0])
    events2.update({i[0]: nn_array})


end = time.time()
print(end - start)

# 446.3999857902527