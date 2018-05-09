import pandas
import geopandas
import rtree
from sys import argv
from shapely.geometry import Point
import os
imprt numpy as np
from sklearn.neighbors import KDTree
import pysql
from osgeo import ogr, gdalconst


# filepath = argv[1]
filepath = '/Users/sudbasnet/Documents/distanceFunction/spatialPrecision/aggregare_event_data_2014_india.csv'
print(filepath)

df = pandas.read_csv(filepath)
geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
crs = {'init': 'epsg:4326'}
gdf = geopandas.GeoDataFrame(df, crs= crs, geometry= geometry)

print(gdf.head())

# index = rtree.index.Index(interleaved = False)
# for fid1 in range(0, )

# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.iterrows.html#pandas.DataFrame.iterrows
# for index, row in gdf.iterrows():


# /Users/sudbasnet/Documents/distanceFunction/spatialPrecision/events_data_write.csv