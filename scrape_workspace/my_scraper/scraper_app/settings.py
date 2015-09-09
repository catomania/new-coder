# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All other settings are here: 
#     http://doc.scrapy.org/topics/settings.html


BOT_NAME = 'livingsocial' # defining a global, app caps = convention for variables we won't be changing

SPIDER_MODULES = ['scraper_app.spiders'] 

ITEM_PIPELINES = ['scraper_app.pipelines.LivingSocialPipeline'] # from pipelines.py

DATABASE = {
	'drivername': 'postgres', # type of db we are using
	'host': 'localhost', 
	'port': '5432', # what port postgres is running
	'username': open('test_username.txt').read(), # fill in username here
	'password': '', # empty on on purpose
	'database': 'scrape' # the db we create in the tutorial

}

print DATABASE.items()