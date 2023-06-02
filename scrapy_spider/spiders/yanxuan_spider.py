# -*- coding:utf-8 -*-
# author:凌陨心
# datetime:2023/5/26 18:02
# software: PyCharm
from scrapy.http import Request

import scrapy
from scrapy_spider.items import YanXuanItem


class YanXuanSpider(scrapy.Spider):
    name = "yanxuan"
    # allowed_domains = ["yx.cbge.top"]
    start_urls = ["https://yx.cbge.top/"]

    # start_urls = ["https://yx.cbge.top/page/9822"]

    def parse(self, response, **kwargs):
        for yanxuan_item in response.xpath('//*[@id="newposts"]/ul[@class="list-group post-list mt-3"]/li'):
            item = YanXuanItem()
            item['title'] = yanxuan_item.xpath("div/h2/a/text()").extract_first()
            item['times'] = yanxuan_item.xpath("span/text()").extract_first()
            href = yanxuan_item.xpath("div/h2/a/@href").extract_first()
            item['href'] = href
            # yield item
            yield Request(url=response.urljoin(href), meta={'yx': item}, callback=self.parse_content)

        next_page = response.css('div.tab-content ul.pagination li')[-1].css('a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_content(self, response):
        item = response.meta['yx']
        item['title'] = response.xpath('//*[@id="body"]/div/div[3]/div[1]/h1/a/text()').extract_first()
        item['types'] = response.xpath('//*[@id="body"]/div/div[3]/div[1]/div/span[5]/a/text()').extract_first()
        item['content'] = "/n".join(response.xpath('//*[@class="thread-content message break-all"]/p/text()').extract())
        yield item

# from scrapy import cmdline
#
# cmdline.execute('scrapy crawl yanxuan'.split())
