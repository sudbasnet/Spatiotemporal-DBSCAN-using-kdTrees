import spatialkdtree
import spatialdbscan
from spatialkdtree import import_data
from time import time
from spatialdbscan import spatialdbscan
from spatialkdtree import generate, prep_dataset
import pandas as pd


start2 = time()
df_st = import_data('data3_india_2014_northeast.csv', ',')
dbscan_st = spatialdbscan(dataframe=df_st, radius=(1000, 100), eps=0.07685, minPts=4, distancetype=('spatial', 'temporal', 'socioeconomic', 'infrastructure'), threshold=(100, 30))
print("everything finished in ", time() - start2, " seconds.")
dataset_dbscan_st = []
dataset = prep_dataset(df_st)
for d in dataset:
    dataset_dbscan_st.append([d[0], d[1], d[2], d[3], dbscan_st[d[0]]])

df_st = pd.DataFrame(dataset_dbscan_st, columns=('uniqueid', 'lon', 'lat', 'event_date', 'cluster'))
df_st.to_csv("dbscan_northeast_st.csv")
