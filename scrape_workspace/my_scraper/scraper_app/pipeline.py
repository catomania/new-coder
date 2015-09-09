#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website livingsocial.com and
save to a database (postgres).

Scrapy pipeline part - stores scraped items in the database
"""

from sqlalchemy.orm import sessionmaker
from models import Deals, db_connect, create_deals_table # all from models.py

class LivingSocialPipeline(object):
	"""Livingsocial pipeline for storing scraped items in the database"""
	def __init__(self):
		"""
		Initializes database connection and sessionmaker.
		Creates deals table.
		"""
		engine = db_connect()
		create_deals_table(engine)
		self.Session = sessionmaker(bind=engine)
		
	def process_item(self, item, spider): 
		"""Save deals in the database.
		
		This method is called for every item pipeline component.
		
		"""
		session = self.Session() # establish session with database
		deal = Deals(**item) # unpack an item (data of our scraped deal)
		
		try:
			session.add(deal) # add deal to our database
			session.commit() # put deal into database and commit transaction
		except:
			session.rollback() # in case something goes awry
			raise
		finally:
			session.close() # whether or not we are successful, close the connection
		return item