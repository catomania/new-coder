"""
API exercise
"""

from __future__ import print_function

import argparse
import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import requests #use this to grab CPI data from FRED
import tablib

CPI_DATA_URL = 'http://research.stlouisfed.org/fred2/data/CPIAUCSL.txt'

#a class is just another object
#it allows us to create a blueprint to create another object: instances
#it also allows us to group like-things together
class CPIData(object):
	"""Abstraction of the CPI data provided by FRED (Federal Reserve Economic Data).
	
	This stores internally only one value per year.
	
	"""
	
	def __init__(self):
		#each year available to the dataset will end up as a simple key-value
		#pair within this dict. We don't really need any order here so going
		#with a plain old dictionary is the best approach. 
		self.year_cpi = {}
		
		# Later on, we will also remember the first and last year we
		# have found in the dataset to handle years prior or after the 
		# documented timespan. 
		self.last_year = None
		self.first_year = None
		
	def load_from_url(self, url, save_as_file=None):
		"""loads data from a given url.
		
		the downloaded file can also be saved into a location for a later
		re-use with the 'save_as_file' parameter specifying a filename.
		
		after fetching the file, this implementation uses load_from_file
		internally.
		"""
		
		#We don't really know how much data we are going to get here, so
		# it is recommended to just keep as little data as possible in memory
		# at all times. Since python-requests supports gzip-compression by
		# default and decoding these chunks on their own isn't easy,
		# we just disable gzip with the empty "Accept-Encoding" header.
		fp = requests.get(url, stream=True,
						  headers={'Accept-Encoding': None}).raw
		
	def load_from_file(self, fp):
		"""Loads CPI data from a given file-like object."""
	
	def get_adjusted_price(self, price, year, current_year=None):
		"""Returns the adapted price from a given year compared to what current
		year has been specified.
		"""


def main():
	"""This function handles the actual logic of this script."""
	
	# Grab CPI/Inflation data.
	
	# Grab API/game platform data.
	
	# Figure out the current price of each platform.
	# This will require looping through each game platform we received, and
	# calculate the adjusted price based on the CPI data we also receive.
	# During this point, we should also validate our data so we do not skew
	# our results.
	
	# Generate a plot/bar graph for the adjusted price data.
	
	# Generate a CSV file to save for the adjusted price data. 