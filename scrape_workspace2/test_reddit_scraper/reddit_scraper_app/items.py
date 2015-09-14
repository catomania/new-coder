#! -*- coding: utf-8 -*-

"""
Test Reddit Scraper

Scrape data from regularly updated website https://www.reddit.com/r/learnpython and
save to a database (postgres).

Scrapy item part - defines container for scraped data.
"""

from scrapy.item import Item, Field


class RedditLearnPython(Item):
    """Reddit container (dictionary-like object) for scraped data"""
    title = Field()
    link = Field()
   