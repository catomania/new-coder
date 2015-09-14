"""
Stack Overflow Spider

Exercise in trying to get more familiar w/ scrapy

"""
import scrapy
import urlparse 

class StackOverFlowSpider(scrapy.Spider):
	name = 'stackoverflow' # name your spider
	start_urls = ['http://stackoverflow.com/questions?sort=votes']
	
	def parse(self, response): # instance method
		for href in response.css('.question-summary h3 a::attr(href)'):
			full_url = response.urlparse.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_question)
			
	def parse_question(self, response):
		yield {
            'title': response.css('h1 a::text').extract()[0],
            'votes': response.css('.question .vote-count-post::text').extract()[0],
            'body': response.css('.question .post-text').extract()[0],
            'tags': response.css('.question .post-tag::text').extract(),
            'link': response.url,
		}
	