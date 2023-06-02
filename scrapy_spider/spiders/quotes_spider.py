# -*- coding:utf-8 -*-
# author:凌陨心
# datetime:2023/4/13 17:03
# software: PyCharm
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/',

    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            # /html/body/div/div[2]/div[1]/div[1]/span[1]
            yield {
                'author': quote.xpath('span/small/text()').get(),
                'tags': quote.xpath('div/a/text()').extract(),
                'text': quote.css('span.text::text').get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)