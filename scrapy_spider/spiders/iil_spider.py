# -*- coding:utf-8 -*-
# author:凌陨心
# datetime:2023/4/13 17:40
# software: PyCharm
import scrapy
from scrapy_spider.items import IllItem
from scrapy.http import Request


class QuotesSpider(scrapy.Spider):
    name = 'ill_craw'
    start_urls = [
        'https://jbk.99.com.cn/buwei/quanshen.html',
        'https://jbk.99.com.cn/buwei/toubu.html',
        'https://jbk.99.com.cn/buwei/jingbu.html',
        'https://jbk.99.com.cn/buwei/sizhi.html',
        'https://jbk.99.com.cn/buwei/fubu.html',
        'https://jbk.99.com.cn/buwei/beibu.html',
        'https://jbk.99.com.cn/buwei/xiongbu.html',
        'https://jbk.99.com.cn/buwei/yaobu.html',
        'https://jbk.99.com.cn/buwei/penqiang.html',
        'https://jbk.99.com.cn/buwei/tunbu.html',
        'https://jbk.99.com.cn/buwei/pifu.html',
        'https://jbk.99.com.cn/buwei/shengzhibuwei.html'
    ]
    addDict = {
        'bingyin.html': 'ill_cause',
        'zhengzhuang.html': 'ill_symptom',
        'jiancha.html': 'ill_check',
        'yufang.html': 'ill_prevent',
        'zhiliao.html': 'ill_cure',
        'jianbie.html': 'ill_identify',
        'bingfazheng.html': 'ill_complication',
    }

    def parse(self, response):
        for quote in response.css('div.list-cont dl'):
            ill_item = IllItem()
            ill_item['ill_name'] = quote.xpath('dd/b/a/text()').get()  # 疾病名称
            ill_item['addr'] = quote.xpath('dd/b/a/@href').get()  # 地址
            ill_item['intro'] = quote.xpath('dd/p/text()').get()  # 简介
            href = 'https://jbk.99.com.cn/' + ill_item['addr']
            yield Request(url=response.urljoin(href), meta={'name': ill_item}, callback=self.parse_ill_detail)

        next_page = response.css('span.l_pa a::attr("href")').get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_ill_detail(self, response):
        ill_item = response.meta['name']
        ill_item['ill_part'] = ','.join(
            response.xpath('//div[@class="del-wrap1"]/dl/dd/p[1]/a/text()').extract()).strip()  # 发病部位
        ill_item['ill_dep'] = ','.join(
            response.xpath('//div[@class="del-wrap1"]/dl/dd/p[2]/a/text()').extract()).strip()  # 就诊科室
        ill_item['ill_med'] = ','.join(
            response.xpath('//div[@class="del-wrap1"]/dl/dd/p[3]/a/text()').extract()).strip()  # 疾病用药
        ill_item['ill_self_test'] = ','.join(
            response.xpath('//div[@class="del-wrap1"]/dl/dd/p[4]/a/text()').extract()).strip()  # 疾病自测
        ill_item['ill_desc'] = ','.join(response.xpath(
            '//div[@class="detail-left"]/div[@class="del-wrap2"]/div[@class="del-cont"]/p/text()').extract()).strip()  # 疾病介绍
        ill_other_addr = response.xpath(
            '//div[@class="detail-left"]/div[@class="del-wrap2"]/div[@class="del-title"]/a/@href').extract()
        ill_item['ill_other_addr'] = [href.split('/')[-1] for href in ill_other_addr]

        for href in ill_other_addr:
            yield Request(url=response.urljoin(href), meta={'name': ill_item}, callback=self.parse_ill_other_info)

    def parse_ill_other_info(self, response):
        ill_item = response.meta['name']
        add = response.url.split('/')[-1]
        ill_summary = ''.join(response.xpath(
            '//div[@class="detail-left"]/div[@class="del-wrap2"]/div[@class="del-cont"]/p/text()').extract())
        ill_item[self.addDict[add]] = ill_summary
        result = self.judgeComplete(ill_item)
        if result:
            ill_item.pop('ill_other_addr')
            ill_item.pop('addr')
            yield ill_item

    def judgeComplete(self, ill_item):
        """
        判断是否抓取完所有页面
        :param ill_item:
        :return:
        """
        addr_list = ill_item['ill_other_addr']
        result: bool = True
        for key in addr_list:
            ret = self.addDict[key] in ill_item
            if False == ret:
                result = False
                break
        return result
