from spatialkdtree import Node, prep, generate, Node, fixed_radius_neighbors, get_bbox
from time import time

events = {}
st = time()
start = time()
dataset = prep('query_result.csv')
print("file read in ", time() - start, " seconds.")
start = time()
kdTree = generate(dataset)
print("tree generated in ", time() - start, " seconds.")
d = (50, 30)
start = time()
for i in dataset:
    nn_array = []
    n = Node.Node(i[0], (i[1], i[2]), i[3])
    nbrs = fixed_radius_neighbors(kdTree, n, d)
    for nbr in nbrs:
        nn_array.append(nbr.id)
    events.update({n.id: nn_array})


print("FRN object generated in ", time() - start, " seconds.")
print("Total time: ", time() - st, " seconds.")
# 4.3154637813568115
# 3.2882208824157715
