import csv

MY_FILE = "../data/sample_sfpd_incident_all.csv"

def parse(raw_file, delimiter):
	"""Parses a raw csv file into a JSON-like object."""
	
	#open csv file
	opened_file = open(raw_file)
	
	#read csv file
	#now can get each element one at a time
	csv_data = csv.reader(opened_file, delimiter=delimiter) #this obj is now an interator
	
	parsed_data = [] #empty list
	
	#next = skip over 1st rows AND put header values into this variabl
	fields = csv_data.next() #data headers, .next method, csv_data is generator
	
	#good example of how adding a call of next 'removes' the first value from the csv_data
	#is 2nd answer from the top: http://stackoverflow.com/questions/14551484/trying-to-understand-python-csv-next
	
	for row in csv_data:
		parsed_data.append(dict(zip(fields, row)))
		#for each loop, we append a dictionary to our list
		#we use built-in zip() to zip together header->value to make dict
		#question: why doesn't this make a (fields, fields) dict the first time? 
	
	return parsed_data
	
	#close csv file	
	opened_file.close()

def main():
	#call our parse function
	new_data = parse(MY_FILE, ",")
	print new_data #ah, python 2.7... 
	
	
	
	#build a data structure to return parsed_data

#call the main function only if you want to run module as a program by command line
if __name__ == "__main__":
	main() 
	
	