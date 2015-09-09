#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website livingsocial.com and
save to a database (postgres).

Database models part - defines tables for storing scraped data.
Direct run will create the table
"""

# Here we setup our database models using SQLAlchemy

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings # gives us access to settings.DATABASE (not settings.py)

def db_connect():
	"""
	Performs database connection using database settings from settings.py
	Returns sqlalchemy engine instance
	"""
	return create_engine(URL(**settings.DATABASE)) # ** unpacks all values within DATABASE dictionary
	# URL function is a constuctor defined in SQLAlchemy, will map keys and values to a URL that
	# SQLAlchemy can understand
	
DeclarativeBase = declarative_base() # map a class that defines our table structure to Postgres

def create_deals_table(engine):
	""""""
	DeclarativeBase.metadata.create_all(engine) 

class Deals(DeclarativeBase): # inherits from DeclarativeBase, uses what we import from sqlalchemy
	"""Sqlalchemy deals model"""
	__tablename__ = "deals"
	
	id = Column(Integer, primary_key=True)
	title = Column('title', String)
	link = Column('link', String, nullable=True)
	location = Column('location', String, nullable=True)
	original_price = Column('original_price', String, nullable=True)
	price = Column('price', String, nullable=True)
	end_date = Column('end_date', DateTime, nullable=True)