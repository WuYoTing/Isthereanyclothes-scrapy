import scrapy


class GuTwSpider(scrapy.Spider):
    name = 'gu-tw'

    def start_requests(self):
        urls = [
            'https://www.gu-global.com/tw/store/search?qbrand=20&qclv1=001'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
