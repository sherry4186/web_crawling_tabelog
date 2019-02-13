# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TabelogSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CookpadImageDownloadItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    recipe_id = scrapy.Field()
    recipe_image_url = scrapy.Field()
