import json
import math
import scrapy
from bs4 import BeautifulSoup


class GuTwSpider(scrapy.Spider):
    name = 'gu-tw'

    # set custom settings
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }
    }

    def __init__(self):
        self.man = '001'
        self.woman = '002'
        self.gu_base_url = 'https://www.gu-global.com/tw/store/'
        self.gu_api_extend_url = 'ApiGetProductInfo.do?format=json&product='
        self.man_prod_url_set = set()

    def start_requests(self):
        url = self.gu_base_url + 'search?qbrand=20&qclv1=' + self.man
        yield scrapy.Request(url=url, callback=self.parse_page_size)
        url = self.gu_base_url + 'search?qbrand=20&qclv1=' + self.woman
        yield scrapy.Request(url=url, callback=self.parse_page_size)

    def parse_page_size(self, response):
        man_index_bs = BeautifulSoup(response.text, "lxml")
        man_prod_amount = int(man_index_bs.select(
            '#content .blkPaginationTop tr th'
        )[0].text.replace('搜尋結果：', '').replace('件', ''))
        man_prod_page = math.ceil(man_prod_amount / 48)
        for page in range(man_prod_page):
            man_page_index = page * 48
            parse_page_url = self.gu_base_url + 'search?qbrand=20&qclv1=001&qstart=' + str(
                man_page_index
            )
            yield scrapy.Request(url=parse_page_url, callback=self.get_prod_url)

    def get_prod_url(self, response):
        man_page_bs = BeautifulSoup(response.text, "lxml")
        for category in man_page_bs.select('#blkMainItemList .unit .info .name a'):
            product_url = category['href']
            if self.gu_base_url + 'goods/' in product_url:
                product_num = product_url.split(self.gu_base_url + 'goods/')[1]
                product_api_url = self.gu_base_url + self.gu_api_extend_url + product_num
                yield scrapy.Request(url=product_api_url, callback=self.get_product_info)

    def get_product_info(self, response):
        jsonresponse = json.loads(response.text)
        if jsonresponse['GoodsInfo']:
            print(jsonresponse['GoodsInfo']['goods']['goodsNm'])
