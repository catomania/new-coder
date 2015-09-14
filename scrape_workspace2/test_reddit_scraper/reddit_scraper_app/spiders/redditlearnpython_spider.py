#! -*- coding: utf-8 -*-

"""
Web Scraper Project
Scrape data from a regularly updated website reddit.com and
save to a database (postgres).
Scrapy spider part - it actually performs scraping.
"""

#more about Scrappy: http://doc.scrapy.org/en/latest/intro/overview.html

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector #for deals_list_xpath
from scrapy.contrib.loader import XPathItemLoader #for loading data into item_fields
from scrapy.contrib.loader.processor import Join, MapCompose #data processing

from reddit_scraper_app.items import RedditLearnPython # importing a class we made

class RedditLearnPythonSpider(BaseSpider): #inherit from scrapy's BaseSpider
	"""Spider for regularly updated reddit.com site, Learn Python subreddit"""
	name = "redditlearnpython"
	allowed_domains = ["reddit.com"]
	start_urls = ["https://www.reddit.com/r/learnpython"] #start crawling here
	
	#deals_list_xpath = '//li[@dealid]' #guiding spider on what to pull from html source
	content_list_xpath = '//*[@id="siteTable"]'
	item_fields = {
        #'title': './/span[@itemscope]/meta[@itemprop="name"]/@content',
        #'link': './/a/@href'
        'title': './/a', #http://stackoverflow.com/questions/2311475/xpath-expression-to-select-text-from-link
        'link': './/a/@href'
	}
	
	def parse(self, response): # actually a method
		"""
		Default callback used by Scrapy to process downloaded response
		
		"""
		         
		selector = HtmlXPathSelector(response) # instantiate HtmlXPathSelector() w/ response parameter
		
		# iterate over deals
		for content in selector.xpath(self.content_list_xpath): #multiple deals per page
			loader = XPathItemLoader(RedditLearnPython(), selector=content) #iterate over each deal
			
			# define processors
			loader.default_input_processor = MapCompose(unicode.strip) #strip out white-space of unicode strings
			loader.default_output_processor = Join() #join data by a space
			
			# iterate over fields and add xpaths to the loader
			for field, xpath in self.item_fields.iteritems(): #itemitems() method allows you to iterate (k, v) of items in a dict
				loader.add_xpath(field, xpath) #add specific field xpath to loader
			yield loader.load_item() # load_item: grabs each item field (link, title, etc), gets xpath, process data
			# w/ input output processor. Yield each item, then move onto next deal