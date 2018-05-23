from spatialkdtree import import_data
from time import time
from spatialdbscan import spatialdbscan


start2 = time()
df = import_data('events_india_2014.csv', ',')
dbscan = spatialdbscan(dataframe=df, radius=(500, 60), eps=0.2, minPts=4, distancetype=('spatial', 'temporal', 'socioeconomic', 'infrastructure'), threshold=(100, 30))
print("everything finished in ", time() - start2, " seconds.")
# 4.3154637813568115
# 3.2882208824157715
