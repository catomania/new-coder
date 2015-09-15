#! -*- coding: utf-8 -*-

"""
Web Scraper Project
Scrape data from a regularly updated website livingsocial.com and
save to a database (postgres).
Scrapy spider part - it actually performs scraping.
"""

#more about Scrappy: http://doc.scrapy.org/en/latest/intro/overview.html

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector #for deals_list_xpath
from scrapy.contrib.loader import XPathItemLoader #for loading data into item_fields
from scrapy.contrib.loader.processor import Join, MapCompose #data processing

from scraper_app.items import LivingSocialDeal # importing a class we made from

class LivingSocialSpider(BaseSpider): #inherit from scrapy's BaseSpider
	"""Spider for regularly updated livingsocial.com site, SF page"""
	name = "livingsocial"
	allowed_domains = ["livingsocial.com"]
	start_urls = ["https://www.livingsocial.com/cities/15-san-francisco"] #start crawling here
	
	deals_list_xpath = '//li[@dealid]' #guiding spider on what to pull from html source
	item_fields = {
        'title': './/span[@itemscope]/meta[@itemprop="name"]/@content',
        'link': './/a/@href',
        'location': './/a/div[@class="deal-details"]/p[@class="location"]/text()',
        'original_price': './/a/div[@class="deal-prices"]/div[@class="deal-strikethrough-price"]/div[@class="strikethrough-wrapper"]/text()',
        'price': './/a/div[@class="deal-prices"]/div[@class="deal-price"]/text()',
        'end_date': './/span[@itemscope]/meta[@itemprop="availabilityEnds"]/@content'
	}
	
	def parse(self, response): # actually a method
		"""
		Default callback used by Scrapy to process downloaded responses
		
		Testing contracts:
		@url http://www.livingsocial.com/cities/15-san-francisco
		@returns items 1
		@scrapes title link
		
		"""
		         
		selector = HtmlXPathSelector(response) # instantiate HtmlXPathSelector() w/ response parameter
		
		# iterate over deals
		for deal in selector.xpath(self.deals_list_xpath): #multiple deals per page
			loader = XPathItemLoader(LivingSocialDeal(), selector=deal) #iterate over each deal
			
			# define processors
			# An Item Loader contains one input processor and one output processor for each (item) field.
			loader.default_input_processor = MapCompose(unicode.strip) #strip out white-space of unicode strings
			loader.default_output_processor = Join() #join data by a space
			
			# iterate over fields and add xpaths to the loader
			for field, xpath in self.item_fields.iteritems(): #itemitems() method allows you to iterate (k, v) of items in a dict
				loader.add_xpath(field, xpath) #add specific field xpath to loader
			yield loader.load_item() # load_item: grabs each item field (link, title, etc), gets xpath, process data
			# w/ input output processor. Yield each item, then move onto next deal