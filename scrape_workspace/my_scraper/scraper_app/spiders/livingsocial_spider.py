#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website livingsocial.com and
save to a database (postgres).

Scrapy spider part - it actually performs scraping.
"""

#more about Scrappy: http://doc.scrapy.org/en/latest/intro/overview.html

from scrapy.spider import BaseSpider

from scraper_app.items import LivingSocialDeal

class LivingSocialSpider(BaseSpider): #inherit from scrapy's BaseSpider
	"""Spider for regularly updated livingsocial.com site, SF page"""
	name = "livingsocial"
	allowed_domains = ["livingsocial.com"]
	start_urls = ["http://www.livingsocial.com/cities/15-san-francisco"]
	
	deals_list_xpath = '//li[@dealid]'
	item_fields = {
		'title': './/span[@itemscope]/meta[@itemprop="name"]/@content',
		'link': './/a/@href',
		'location': './/a/div[@class="deal-details"]/p[@class="location"]/text()',
		'original_price': './/a/div[@class="deal-details"]/div[@class=deal-strikethrough-price"]/div[@class="strikethrough-wrapper"]/text()',
		'price': './/a/div[@class=deal-prices"]/div[@class="deal-price"]/text(),
		'end_date': './/span[@itemscope]/meta[@itemprop="availabilityEnds"]/@content'
	}