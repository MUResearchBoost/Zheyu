# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MuFacultyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    prof_page = scrapy.Field()
    prof_name = scrapy.Field()
    prof_title = scrapy.Field()
    prof_email = scrapy.Field()
    prof_phone = scrapy.Field()
    prof_department = scrapy.Field()

