"""
API exercise
"""

from __future__ import print_function

import argparse
import logging
import os

import matplotlib.pylot as plt
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