"""
Stack Overflow Spider

Exercise in trying to get more familiar w/ scrapy

"""
import scrapy

class StackOverFlowSpider(scrapy.Spider):
	name = 'stackoverflow'
	start_urls = ['https://stackoverflow.com/questions?sort=votes']
	
	def parse(self, response):
		for href in response.css('.question-summary h3 a::attr(href)'):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_question)
			
	def parse_question(self, response):
		yield {
			'title': response.css('h1 a::text').extract()[0]
		
		}
	