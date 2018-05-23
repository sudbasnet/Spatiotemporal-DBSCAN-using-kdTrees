import queue
from distancefunction import distancefunction
from spatialkdtree import generate, prep_dataset, get_frnn
from distancefunction import prep_events
from time import time


# this spatialdbscan takes in the events set, the frnn object created by spatialkdtree and, the eps and minPts
# limits = (spatial threshold in km, temporal threshold in days)
def spatialdbscan(dataframe, radius, eps, minPts, distancetype, threshold):
    start = time()
    dataset = prep_dataset(dataframe)
    print("dataset generated in ", time() - start, " seconds.")
    # print(dataset[3])
    events = prep_events(dataframe, sociovar_count=2, infravar_count=6)
    # print(events[dataset[3][0]])
    start = time()
    print("generating tree")
    tree = generate(dataset)
    print("tree generated in ", time() - start, " seconds.")
    start = time()
    frnn = get_frnn(dataset, tree, radius)
    print("frnn generated in ", time() - start, " seconds.")
    # print(frnn[dataset[3][0]])
    start = time()
    dbscan_clustering = {}
    for key, event in events.items():
        # print("wtf")
        dbscan_clustering.update({key: 0})
    visited = []
    print("dbscan object generated in ", time() - start, " seconds.")
    cluster_number = 0
    start = time()
    for key, event in events.items():
        cluster = []
        q = queue.Queue()
        if key not in visited and dbscan_clustering[key] == 0 and len(frnn[key]) >= minPts:
            q.put(key)
            while not q.empty():
                current_event_id = q.get()
                frnn_neighbors = frnn[current_event_id]
                neighbors = [current_event_id]
                for frnn_n in frnn_neighbors:
                    # if frnn_n not in visited:
                    d = distancefunction(events[current_event_id], events[frnn_n], distancetype, threshold)
                    if d <= eps:
                        neighbors.append(frnn_n)
                if len(neighbors) >= minPts:
                    visited.append(current_event_id)
                    for n in neighbors:
                        if n not in cluster:
                            cluster.append(n)
                            q.put(n)
        if len(cluster) >= minPts:
            cluster_number += 1
            print("Cluster ", cluster_number, " formed.")
            for c in cluster:
                dbscan_clustering[c] = cluster_number
    print("dbscan clustering generated in ", time() - start, " seconds.")
    return dbscan_clustering
