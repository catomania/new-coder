""" Data Visualization Project
Parse data from CSV file and make charts and plot on a map!

Part 3: here we parse through each line and and create a geoson obj,

to be collected into 1 geojson file for uploading into gist.github.com
"""

import geojson #ideally we could just import the dumps part

import parse as p  #make it shorter!

#the function create_map(data_file) parses through our data file to create a 
#GeoJSON file.

def create_map(data_file):
	#define type of GeoJSON we're creating (a collection of features)
	geo_map = {"type": "FeatureCollection"}
	
	#define empty list to collect each point to graph
	
	# Iterate over our data to create GeoJSON document
	
	#We are using enumerate() so we get the line, as well
	#as the index, which is the line number
	
		#skip any zero coordinates as this will throw off our map
		#setup a new dict for each iteration
		#assign line items for appropriate GeoJSON fields
		#add data dict to our item_list
	
	#for each point in our item_list, we add the point to our
	#dict. setdefault creates a key called 'features' that
	#has a value type of an empty list. with each iteration, we
	#are appending our point to that list
	
	#now that all data is parsed into GeoJSON, write to a file so we
	#can upload it to gist.github.com (what is this????)