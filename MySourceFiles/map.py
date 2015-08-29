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
	item_list = []
	
	# Iterate over our data to create GeoJSON document
	
	#We are using enumerate() so we get the line, as well
	#as the index, which is the line number
	#for every line in data_file, we take certain values that X, Y, Category, etc
	#and assign it to a key that GeoJSON requires (type, id)
	#however, if either line['X'] or line['Y'] is 0, we skip over it (continue)
	for index, line in enumerate(data_file):
	
		#skip any zero coordinates as this will throw off our map
		if line['X'] == "0" or line['Y'] == "0":
			continue
		
		#setup a new dict for each iteration
		data = {}
		#assign line items for appropriate GeoJSON fields
		data['type'] = 'Feature'
		data['id'] = index #possible because of enumerate()
		data['properties'] = {'title': line['Category'],
							  'description': line['Descript'],
							  'date': line['Date']}
		data['geometry'] = {'type': 'Point',
							'coordinates': (line['X'], line['Y'])}
		
		#add data dict to our item_list
		item_list.append(data)
	
	#next, we will build onto our geo_map dict by adding our points from item_list
	#for each point in our item_list, we add the point to our
	#dict. setdefault creates a key called 'features' that
	#has a value type of an empty list. With each iteration, we
	#are appending our point to that list
	
	for point in item_list:
		geo_map.setdefault('features', []).append(point)
		
		#setdefault method: sets a key to features and its value as an empty list
		#with each iteration, we append the point to the list
	
	#now that all data is parsed into GeoJSON, write to a file so we
	#can upload it to gist.github.com (what is this????)
	with open('file_sf.geojson', 'w') as f:
		f.write(geojson.dumps(geo_map))

def main():
	data = p.parse(p.MY_FILE, ",")
	return create_map(data)
if __name__ == "__main__":
	main()