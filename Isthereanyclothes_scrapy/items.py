# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class IsthereanyclothesScrapyItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass


class ClothesItem(Item):
    prod_number = Field()
    brand_id = Field()
    sex = Field()
    name = Field()
    description = Field()
    material = Field()
    url = Field()
    size_url = Field()


class ClothesPriceLogItem(Item):
    prod_number = Field()
    price = Field()


class ClothesImagesItem(Item):
    prod_number = Field()
    type = Field()
    url = Field()


class ClothesProdStatusItem(Item):
    prod_number = Field()
    is_new_prod = Field()
    is_online_only = Field()
    is_set = Field()
    is_limited_time = Field()
    is_price_down = Field()
    can_modify = Field()
    limited_price_date = Field()
