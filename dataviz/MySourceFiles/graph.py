"""
Data Visualization Project

Parse data from an ugly CSV or Excel file, and render it in
JSON-like form, visualize in graphs, and plot on Google Maps.

Part II: take the data we just parsed (from parse.py) and visualize it
using popular Python math libraries
"""

from collections import Counter #standard library module

import csv
import matplotlib.pyplot as plt
import numpy as np

MY_FILE = "../data/sample_sfpd_incident_all.csv"

def parse(raw_file, delimiter):
	"""Parses a raw csv file into a JSON-like object"""
	
	#open csv file, later on we'll close it
	opened_file = open(raw_file)
	
	#read csv data
	csv_data = csv.reader(opened_file, delimiter=delimiter)
	
	#setup empty list
	parsed_data = []
	
	#skip over the header row, but set this variable as header row (what next does)
	fields = csv_data.next()
	
	#iterate over each row of the csv file, zip together field->value
	for row in csv_data: #remember, now csv_data doesn't have a header anymore
		parsed_data.append(dict(zip(fields, row)))
		
	#close the csv file
	opened_file.close()
	
	return parsed_data #will be in JSON-like format

def visualize_days():
	"""visualize data by day of week"""
	data_file = parse(MY_FILE, ",") #uses the parse function above
	#returns a dict where it sums total values for each key
	#in this case, keys are dayofweek, values are count of incidents
	#count of incidents
	
	counter = Counter(item["DayOfWeek"] for item in data_file) #counter = container
	#the Counter keeps track of how many times equivalent values are added
	#counter is a dict subclass for counting hashable objects
	
	#separate out counter in order to correctly plot it
	data_list = [
					counter["Monday"],
					counter["Tuesday"],
					counter["Wednesday"],
					counter["Thursday"],
					counter["Friday"],
					counter["Saturday"],
					counter["Sunday"]
				]
	
	day_tuple = tuple(["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]) 
	#a tuple is a sequence of immutable python objects, cannot be changed
	
	#assign data to a plot
	#plt = matplotlib.pyplot
	plt.plot(data_list)
	
	#assign labels to plot from day_list
	plt.xticks(range(len(day_tuple)), day_tuple) #plot tick labels 
	
	#save the graph!
	plt.savefig("Days.png")
	
	#close figure
	plt.clf()

def visualize_type():
	"""visualize data by category in bar graph"""
	data_file = parse(MY_FILE, ",")
	
	#returns a dict where it sums total incidents per category
	counter = Counter(item["Category"] for item in data_file)
	
	#set the labels which are based off of our counter keys
	labels = tuple(counter.keys()) 
	
	#set where labels hit the x-axis
	xlocations = np.arange(len(labels)) + 0.5 
	#arange = return evenly spaced values when given interval
	
	#width of each bar
	width = 0.5
	
	#assign data to bar plot
	plt.bar(xlocations, counter.values(), width=width)
	
	#assign labels and tick locations to x-axis
	plt.xticks(xlocations + width / 2, labels, rotation=90)
	
	#give some more room so labels aren't cut off in graph
	plt.subplots_adjust(bottom=0.4)
	
	#make overall graph/figure larger
	plt.rcParams['figure.figsize'] = 12, 8 
	
	#save graph
	plt.savefig("Type.png")
	
	#close figure
	plt.clf()

def main():
	# call the 2 main functions we just wrote
	visualize_days()
	visualize_type() 

if __name__ == "__main__": #if this is main and not being imported as module
	main() #then call the main function that runs the other 2 new functions