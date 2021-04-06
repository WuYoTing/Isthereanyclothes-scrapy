import math
import scrapy
from bs4 import BeautifulSoup


class GuTwSpider(scrapy.Spider):
    name = 'gu-tw'

    def __init__(self):
        self.gu_base_link = 'https://www.gu-global.com/tw/store/'
        self.man_prod_url_set = set()

    def start_requests(self):
        url = self.gu_base_link + 'search?qbrand=20&qclv1=001'
        yield scrapy.Request(url=url, callback=self.parse_page_size)

    def parse_page_size(self, response):
        man_index_bs = BeautifulSoup(response.text, "lxml")
        man_prod_amount = int(
            man_index_bs.select('#content .blkPaginationTop tr th')[0].text.replace(
                '搜尋結果：', '').replace('件', ''))
        man_prod_page = math.ceil(man_prod_amount / 48)
        for page in range(man_prod_page):
            man_page_index = page * 48
            url = self.gu_base_link + 'search?qbrand=20&qclv1=001&qstart=' + str(man_page_index)
            yield scrapy.Request(url=url, callback=self.parse_page_size)

    def parse_prod_url(self, response):
        man_page_bs = BeautifulSoup(response.text, "lxml")
        for category in man_page_bs.select('#blkMainItemList .unit .info .name a'):
            category_url = category['href']
            if self.gu_base_link + 'goods/' in category_url:
                self.man_prod_url_set.add(category_url)
                print(category_url)
