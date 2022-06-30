# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):

    name = scrapy.Field()
    person_info = scrapy.Field()
    score = scrapy.Field()
    desc = scrapy.Field()
