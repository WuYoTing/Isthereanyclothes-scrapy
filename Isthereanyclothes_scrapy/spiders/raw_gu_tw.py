import random
import math
import scrapy
from bs4 import BeautifulSoup

import Isthereanyclothes_scrapy.items as items


class RawGuTwSpider(scrapy.Spider):
    name = 'raw-gu-tw'

    # set custom settings
    custom_settings = {
        'DOWNLOAD_DELAY': random.uniform(0.7, 1),
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }
    }

    def __init__(self):
        self.man = '001'
        self.woman = '002'
        self.man_size = 0
        self.woman_size = 0
        self.gu_base_url = 'https://www.gu-global.com/tw/store/'
        self.gu_api_extend_url = 'ApiGetProductInfo.do?product='

    def start_requests(self):
        man_index_url = self.gu_base_url + 'search?qbrand=20&qclv1=' + self.man
        yield scrapy.Request(
            url=man_index_url,
            priority=1,
            cb_kwargs=dict(sex=1),
            callback=self.parse_page_size
        )
        woman_index_url = self.gu_base_url + 'search?qbrand=20&qclv1=' + self.woman
        yield scrapy.Request(
            url=woman_index_url,
            priority=2,
            cb_kwargs=dict(sex=2),
            callback=self.parse_page_size
        )

    def parse_page_size(self, response, sex):
        man_index_bs = BeautifulSoup(response.text, "lxml")
        man_prod_amount = int(man_index_bs.select(
            '#content .blkPaginationTop tr th'
        )[0].text.replace('搜尋結果：', '').replace('件', ''))
        man_prod_page = math.ceil(man_prod_amount / 48)

        if sex == 1:
            sex_code = self.man
            print('男 共 ' + str(man_prod_page) + ' 頁 ' + str(man_prod_amount) + " 個產品" + '  ' + str(
                response.status))
        elif sex == 2:
            sex_code = self.woman
            print('女 共 ' + str(man_prod_page) + ' 頁 ' + str(man_prod_amount) + " 個產品" + '  ' + str(
                response.status))

        for page in range(man_prod_page):
            page_index = page * 48
            parse_page_url = self.gu_base_url + 'search?qbrand=20&qclv1=' + sex_code + '&qstart=' + str(
                page_index)
            yield scrapy.Request(
                url=parse_page_url,
                priority=3,
                cb_kwargs=dict(sex=sex),
                callback=self.get_prod_url
            )

    def get_prod_url(self, response, sex):
        man_page_bs = BeautifulSoup(response.text, "lxml")
        for category in man_page_bs.select('#blkMainItemList .unit .info .name a'):
            product_url = category['href']
            if self.gu_base_url + 'goods/' in product_url:
                product_num = product_url.split(self.gu_base_url + 'goods/')[1]
                product_api_url = self.gu_base_url + self.gu_api_extend_url + product_num
                if sex == 1:
                    self.man_size += 1
                    print('man ' + str(product_api_url) + ' ' + str(
                        response.status) + ' ' + str(self.man_size))
                    yield scrapy.Request(
                        url=product_api_url,
                        priority=4,
                        cb_kwargs=dict(sex=sex),
                        callback=self.get_product_info
                    )
                elif sex == 2:
                    self.woman_size += 1
                    print('woman ' + str(product_api_url) + ' ' + str(
                        response.status) + ' ' + str(self.woman_size))
                    yield scrapy.Request(
                        url=product_api_url,
                        priority=4,
                        cb_kwargs=dict(sex=sex),
                        callback=self.get_product_info
                    )

    def get_product_info(self, response, sex):
        json_resp = response.json()
        
        print(json_resp)
