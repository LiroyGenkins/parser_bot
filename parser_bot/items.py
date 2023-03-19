# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProblemItem(scrapy.Item):
    # define the fields for your item here like:
    problem_name = scrapy.Field()
    problem_number = scrapy.Field()
    solves = scrapy.Field()
    problem_link = scrapy.Field()
    themes = scrapy.Field()
    rating = scrapy.Field()
