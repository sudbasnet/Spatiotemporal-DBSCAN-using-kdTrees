# spatiotemporal-kdTree
1. Imports a file with first 4 columns [uniqueid, longitude, latitude, date (in YYYYMMDD), ...]
2. forms a kd-Tree based on the lat, lon and date (treats all as numeric)
3. performs fixed-radius neighborhood search
4. distance must be a tuple: distance = (spatial distance in km, temporal distance in days)
