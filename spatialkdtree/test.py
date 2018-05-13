from spatialkdtree.Node import prep, generate, Node, fixed_radius_neighbors
from time import time

events = {}
dataset = prep('events_data_write.csv')
kdTree = generate(dataset)
d = (100, 30)
start = time()
for i in dataset:
    nn_array = []
    n = Node(i[0], (i[1], i[2]), i[3])
    nbrs = fixed_radius_neighbors(kdTree, n, d)
    for nbr in nbrs:
        nn_array.append(nbr.id)
    events.update({n.id: nn_array})


end = time()
print(end - start)
# 4.3154637813568115
