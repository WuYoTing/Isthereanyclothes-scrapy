import scrapy
import bs4
import math


class GuTwSpider(scrapy.Spider):
    name = 'gu-tw'
    allowed_domains = ['www.gu-global.com/tw']
    start_urls = ['https://www.gu-global.com/tw/store/search?qbrand=20&qclv1=001']

    def parse(self, response):
        man_index_bs = bs4.BeautifulSoup(response.text, "lxml")
        man_prod_amount = int(
            man_index_bs.select('#content .blkPaginationTop tr th')[0].text.replace(
                '搜尋結果：', '').replace('件', ''))
        man_prod_page = math.ceil(man_prod_amount / 48)
        print(man_prod_amount + ' : ' + man_prod_page)
