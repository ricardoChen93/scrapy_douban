# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Movie(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    performer = scrapy.Field()
    genre = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    release_date = scrapy.Field()
    film_length = scrapy.Field()
    summary = scrapy.Field()
    rating = scrapy.Field()
