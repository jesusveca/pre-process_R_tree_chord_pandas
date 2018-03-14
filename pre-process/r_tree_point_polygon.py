import timeit
import pandas as pd
from sqlalchemy import create_engine
import geopandas as gpd
import geojson
from rtree import index
from pprint import pprint
from shapely.geometry import *
import json
import csv
import shapely.speedups
shapely.speedups.enable()


#### extract only polygons from community districts.geojson
polygons_p = gpd.GeoDataFrame.from_file('distritos.geojson')
polygons = polygons_p["geometry"]       # Polygons of each Boro

#### read and add extra information of each community district
filename="distritos.geojson"
with open (filename, "r") as myfile:
    data=myfile.read()

#### create the index for rTree
dataset = json.loads(data)
idx = index.Index()
count = -1
#### insert in rtree only the index and bounding box of each polygon
for f in dataset["features"]:
    count +=1
    idx.insert(count, f["bbox"])
#### insert in rtree only the index and bounding box of each polygon



###### load the points
file = 'sample_merged_1.csv'
csv_database = create_engine('sqlite:///points_database.db')
###### load the points

########### create and add database
# chunksize = 100000
# i = 0
# j = 1
# for df in pd.read_csv(file, chunksize=chunksize, iterator=True):
#       df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
#       df.index += j
#       i+=1
#       df.to_sql('table', csv_database, if_exists='append')
#       j = df.index[-1] + 1
########### create and add database

########## query df
df = pd.read_sql_query("""
                        SELECT
                            pickup_long, pickup_lat, dropoff_long, dropoff_lat
                        FROM "table"
                        WHERE
                            pickup_long IS NOT NULL

                        """
                    , csv_database)
print (len(df))
total_of_set_points = len(df)
###### load the points



# # ######time
start = timeit.default_timer()
# # ######time



# # ########### storage and create .csv file
f = open("only_orig_desti.csv", 'wt')
writer = csv.writer(f)
writer.writerow( ('Origin','Destination') )


###### Function that returns the boroCD
def find_boroCD(point):
    for j in idx.intersection([point.x, point.y]):  ##### if exists any intersection with bbox and the point
        if(point.within(polygons[j])): #### if the polygon contain a point
            #number_of_polygon = j      #bbox_of_polygon_boro = dataset["features"][j]["bbox"]
            name_of_borough = dataset["features"][j]["properties"]["BoroCD"]
            return name_of_borough
            break;
###### Function that returns the boroCD


###### query
for s in range (total_of_set_points):
    pickup_long = df["pickup_long"][s]
    pickup_lat  = df["pickup_lat"][s]
    dropoff_long= df["dropoff_long"][s]
    dropoff_lat = df["dropoff_lat"][s]

    point   = Point(pickup_long, pickup_lat)
    point_2 = Point(dropoff_long, dropoff_lat)

    name_of_borough_point_1 = find_boroCD(point)
    name_of_borough_point_2 = find_boroCD(point_2)

    if (name_of_borough_point_1 and name_of_borough_point_2):
        writer.writerow( (name_of_borough_point_1,name_of_borough_point_2))
###### query


# ######time
stop = timeit.default_timer()
execution_time = stop - start
print("\n"+str(execution_time)+" secs")
# # ######time
