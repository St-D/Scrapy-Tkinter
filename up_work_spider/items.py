# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity
from unicodedata import normalize
from re import sub


def strip_other(x):
    return str(sub(r'[\n\t]', '', x)).strip()



class UpWItem(scrapy.Item):
    name_project = scrapy.Field()
    url_to_project = scrapy.Field()
    price = scrapy.Field()
    level = scrapy.Field()
    crawl_date = scrapy.Field()
    show_status = scrapy.Field()


class ScrapTstLoader(ItemLoader):
    default_item_class = UpWItem
    # default_input_processor = Identity()
    # default_input_processor = MapCompose(lambda x: normalize('NFKD', unicode(x)))
    # default_input_processor = MapCompose(lambda x: str(x), lambda x: normalize('NFC', x.decode('utf-8')))
    # default_input_processor = MapCompose(lambda x: normalize('NFC', x.decode('utf-8')))
    # default_input_processor = MapCompose(unicode.string)
    # default_input_processor = MapCompose(strip_dashes)

    crawl_date_in = Identity()
    show_status_in = Identity()

    default_input_processor = MapCompose(lambda x: str(sub(r'[\n\t]', '', x)).strip())
    default_output_processor = TakeFirst()
