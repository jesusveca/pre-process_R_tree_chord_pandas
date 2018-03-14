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


# #### extract only polygons from community districts.geojson
# polygons_p = gpd.GeoDataFrame.from_file('distritos.geojson')
# polygons = polygons_p["geometry"]       # Polygons of each Boro
#
# #### read and add extra information of each community district
# filename="distritos.geojson"
# with open (filename, "r") as myfile:
#     data=myfile.read()
#
# #### create the index for rTree
# dataset = json.loads(data)
# idx = index.Index()
# count = -1
# #### insert in rtree only the index and bounding box of each polygon
# for f in dataset["features"]:
#     count +=1
#     idx.insert(count, f["bbox"])
# #### insert in rtree only the index and bounding box of each polygon
#
#
#
# ###### load the points
# file = 'sample_merged_1.csv'
# csv_database = create_engine('sqlite:///csv_database.db')
# ###### load the points
#
# ########### create and add database
# # chunksize = 100000
# # i = 0
# # j = 1
# # for df in pd.read_csv(file, chunksize=chunksize, iterator=True):
# #       df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
# #       df.index += j
# #       i+=1
# #       df.to_sql('table', csv_database, if_exists='append')
# #       j = df.index[-1] + 1
# ########### create and add database
#
# ########## query df
# df = pd.read_sql_query("""
#                         SELECT
#                             Pickup_longitude, Pickup_latitude, Dropoff_longitude, Dropoff_latitude
#                         FROM "table"
#                         WHERE
#                             Pickup_longitude IS NOT NULL
#                         """
#                     , csv_database)
# print (len(df))
# total_of_set_points = len(df)
# ###### load the points
#
#
#
# # # ######time
start = timeit.default_timer()
# # # ######time
#
#
# # # # ########### storage and create .csv file
# f = open("only_orig_desti.csv", 'wt')
# writer = csv.writer(f)
# writer.writerow( ('Origin','Destination') )
# # # # ########### storage and create .csv file
#
# # ###### Function that returns the boroCD
# def find_boroCD(point):
#     for j in idx.intersection([point.x, point.y]):  ##### if exists any intersection with bbox and the point
#         if(point.within(polygons[j])): #### if the polygon contain a point
#             #number_of_polygon = j      #bbox_of_polygon_boro = dataset["features"][j]["bbox"]
#             name_of_borough = dataset["features"][j]["properties"]["BoroCD"]
#             return name_of_borough
#             break;
# # ###### Function that returns the boroCD
#
#
# # ###### query
# for s in range (total_of_set_points):
#     pickup_long = df["Pickup_longitude"][s]
#     pickup_lat  = df["Pickup_latitude"][s]
#     dropoff_long= df["Dropoff_longitude"][s]
#     dropoff_lat = df["Dropoff_latitude"][s]
#
#     point   = Point(pickup_long, pickup_lat)
#     point_2 = Point(dropoff_long, dropoff_lat)
#
#     name_of_borough_point_1 = find_boroCD(point)
#     name_of_borough_point_2 = find_boroCD(point_2)
#
#     if (name_of_borough_point_1 and name_of_borough_point_2):
#         writer.writerow( (name_of_borough_point_1,name_of_borough_point_2))
# ###### query



# # ########## load points
# set_of_points = pd.read_csv("only_orig_desti.csv")
# # ########## count origin and destination trips
# counter = set_of_points.groupby(set_of_points.columns.tolist()).size().reset_index().rename(columns={0:'count'})
# # ########## count origin and destination trips
# #
# # # ########### storage and create .csv file
# f = open("counter_orig_destin_FINAL.csv", 'wt')
# writer = csv.writer(f)
# writer.writerow( ('Origin','Destination','Count') )
# # # ########### storage and create .csv file
# #
# # ########## write into .csv
# for x in range(len(counter)):
#     origin = counter["Origin"][x]
#     destination = counter["Destination"][x]
#     contador = counter["count"][x]
#     if (destination!=0):
#         # if (contador>50):
#         writer.writerow( (origin,destination,contador) )
# # ########## write into .csv



########## verify if the total of registers is equal to the final count
##########count the total of registers in .csv
# contador_GENERAL = pd.read_csv("counter_orig_destin_FINAL.csv")
# cont = 0
# for pp in range (len(contador_GENERAL)):
    # cont = cont + contador_GENERAL["Count"][pp]
# print (cont)
##########count the total of registers in .csv



######### create a .csv with origin, destination, count, and the name of place (eg Manhattan)
f = open("counter_final_NOMBRE_BOROCD.csv", 'wt')
writer = csv.writer(f)
writer.writerow( ('id_origin', 'id_destino', 'times') )

with open('counter_orig_destin_FINAL.csv') as File:
    reader = csv.reader(File)
    for row in reader:
        nombre_origin = row[0]
        nombre_destinatio = row[1]
        # print (row)
        with open('community_board_by_borough.csv') as F:
            other_reader = csv.reader(F)
            for row_1 in other_reader:
                str_final_1 = ""
                if nombre_destinatio == row_1[0] :
                    if nombre_origin != nombre_destinatio: ## we dont count the same community districts
                    # if row_1[2]!=' "Park"': ## parks dont count
                        if row[2]>'3': ## number of trips greather than 3
                            str_final_1 = row_1[0] + " /" + row_1[1] + "/"
                            writer.writerow( (row[0], str_final_1, row[2]) )
######### create a .csv with origin, destination, count, and the name of place (eg Manhattan)


# ######time
stop = timeit.default_timer()
execution_time = stop - start
print("\n"+str(execution_time)+" secs")
# # ######time
