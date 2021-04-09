# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IsthereanyclothesScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ClothesItem(scrapy.Item):
    prod_number = scrapy.Field()
    brand_id = scrapy.Field()
    sex = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    material = scrapy.Field()
    url = scrapy.Field()
    size_url = scrapy.Field()


class ClothesPriceLogItem(scrapy.Item):
    price = scrapy.Field()


class ClothesImagesItem(scrapy.Item):
    type = scrapy.Field()
    url = scrapy.Field()


class ClothesSaleTagItem(scrapy.Item):
    is_new_prod = scrapy.Field()
    is_online_only = scrapy.Field()
    is_new_prod = scrapy.Field()
    is_set = scrapy.Field()
    is_limited_time = scrapy.Field()
    is_price_down = scrapy.Field()
    can_modify = scrapy.Field()
    limited_price_date = scrapy.Field()
