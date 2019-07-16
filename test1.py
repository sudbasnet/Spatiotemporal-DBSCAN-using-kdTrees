import spatialkdtree
import spatialdbscan
from spatialkdtree import import_data
from time import time
from spatialdbscan import spatialdbscan
from spatialkdtree import generate, prep_dataset
import pandas as pd


start2 = time()
df_st = import_data('events_india_2014.csv', ',')
eps = 0.05
minPts = 5
dbscan_st = spatialdbscan(dataframe=df_st, radius=(500, 60), eps=eps, minPts=minPts, distancetype=('spatial', 'temporal', 'socioeconomic', 'infrastructure'), threshold=(100, 30), sociovar_count=2, infravar_count=6)
print("everything finished in ", time() - start2, " seconds.")
df_st_t = import_data('events_india_2014.csv', ',')
df_st_t["cluster"] = None
for index, row in df_st_t.iterrows():
	df_st_t.loc[index, "cluster"] = dbscan_st[row[0]]


df_st_t.to_csv("clustering_final_"+ str(eps) + "_" + str(minPts) + "_st.csv")
start2 = time()
dbscan_st = spatialdbscan(dataframe=df_st, radius=(500, 60), eps=eps, minPts=minPts, distancetype=('spatial', 'temporal', 'socioeconomic'), threshold=(100, 30), sociovar_count=2, infravar_count=6)
print("everything finished in ", time() - start2, " seconds.")
df_st_t = import_data('events_india_2014.csv', ',')
df_st_t["cluster"] = None
for index, row in df_st_t.iterrows():
	df_st_t.loc[index, "cluster"] = dbscan_st[row[0]]


df_st_t.to_csv("clustering_final_"+ str(eps) + "_" + str(minPts) + "_st_se.csv")
start2 = time()
dbscan_st = spatialdbscan(dataframe=df_st, radius=(500, 60), eps=eps, minPts=minPts, distancetype=('spatial', 'temporal', 'socioeconomic', 'infrastructure'), threshold=(100, 30), sociovar_count=2, infravar_count=6)
print("everything finished in ", time() - start2, " seconds.")
df_st_t = import_data('events_india_2014.csv', ',')
df_st_t["cluster"] = None
for index, row in df_st_t.iterrows():
	df_st_t.loc[index, "cluster"] = dbscan_st[row[0]]


df_st_t.to_csv("clustering_final_"+ str(eps) + "_" + str(minPts) + "_st_se_in.csv")