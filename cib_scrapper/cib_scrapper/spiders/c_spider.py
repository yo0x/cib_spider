import scrapy
import os

URL1 = os.environ['URL1']
CIB_USER=os.environ['cib_user']
CIB_PASS=os.environ['cib_pass']

class C_spider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            URL1,
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')