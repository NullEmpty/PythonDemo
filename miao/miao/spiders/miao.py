import scrapy
from scrapy import Selector
from scrapy import Request

from miao.items import ContentItem


class NgaSpider(scrapy.Spider):
    name = "NgaSpider"
    host = "http://bbs.ngacn.cc/"
    start_urls = [
        "http://bbs.ngacn.cc/thread.php?fid=406",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        selector = Selector(response)
        content_list = selector.xpath("//*[@class='topic']")
        for content in content_list:
            topic = content.xpath('string(.)').extract_first()
            print(topic)
            url = self.host + content.xpath('@href').extract_first()
            print(url)
            yield Request(url=url, callback=self.parse_topic)

    def parse_topic(self, response):
        seletor = Selector(response)
        content_list = seletor.xpath("//*[@class='postcontent ubbcode']")
        for content in content_list:
            content = content.xpath('string(.)').extract_first()
            #print(content)
            item = ContentItem()
            item['url'] = response.url
            item['content'] = content
            item['author'] = "author"
            yield item

