"""
API exercise
"""

from __future__ import print_function

import argparse
import logging
import os

import matplotlib.pylot as plt
import numpy as np
import requests
import tablib

CPI_DATA_URL = 'http://research.stlouisfed.org/fred2/data/CPIAUCSL.txt'


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