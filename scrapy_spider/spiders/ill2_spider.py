# -*- coding:utf-8 -*-
# author:凌陨心
# datetime:2023/4/14 11:43
# software: PyCharm

import scrapy


class IllsetsSpider(scrapy.Spider):
    name = "illsets"
    allowed_domains = ["jbk.99.com.cn"]
    start_urls = ["https://jbk.99.com.cn/tnb/"]
    titlesDict = {
        'bingyin.html': '病因',
        'zhengzhuang.html': '症状',
        'jiancha.html': '检查',
        'yufang.html': '预防',
        'zhiliao.html': '治疗',
        'jianbie.html': '鉴别',
        'bingfazheng.html': '并发症',
    }

    def parse(self, response):
        title = response.xpath('//div[@class="del-wrap1"]/b/text()').extract()[0].strip()  # 疾病名称
        ill_part = ','.join(response.xpath('//div[@class="del-wrap1"]/dl/dd/p[1]/a/text()').extract()).strip()  # 发病部位
        dep_name = ','.join(response.xpath('//div[@class="del-wrap1"]/dl/dd/p[2]/a/text()').extract()).strip()  # 就诊科室
        ill_medicine = ','.join(
            response.xpath('//div[@class="del-wrap1"]/dl/dd/p[3]/a/text()').extract()).strip()  # 疾病用药
        ill_test = ','.join(response.xpath('//div[@class="del-wrap1"]/dl/dd/p[4]/a/text()').extract()).strip()  # 疾病自测
        ill_summary = \
        response.xpath('//div[@class="detail-left"]/div[@class="del-wrap2"]/div[@class="del-cont"]/p/text()').extract()[
            0].strip()
        ill_analysis = response.xpath(
            '//div[@class="detail-left"]/div[@class="del-wrap2"]/div[@class="del-title"]/a/@href').extract()

        item = {'疾病名称': title, '发病部位': ill_part, '就诊科室': dep_name, '疾病用药': ill_medicine,
                '疾病自测': ill_test, '疾病描述': ill_summary}
        # '/baidianfeng/bingyin.html,/baidianfeng/zhengzhuang.html,/baidianfeng/jiancha.html,/baidianfeng/yufang.html,
        # /baidianfeng/zhiliao.html,/baidianfeng/jianbie.html,/baidianfeng/bingfazheng.html'
        titles = []
        for href in ill_analysis:
            title = self.titlesDict[href.split('/')[-1]]
            titles.append(title)
        item['titles'] = titles

        for href in ill_analysis:
            full_url = response.urljoin(href)
            yield scrapy.Request(full_url,callback=self.parse_others,meta={'item':item})

    def parse_others(self, response):

        ill_summary = ''.join(response.xpath('//div[@class="detail-left"]/div[@class="del-wrap2"]/div[@class="del-cont"]/p/text()').extract())
        title = self.titlesDict[response.url.split('/')[-1]]
        item = response.meta['item']
        item[title] = ill_summary
        result = self.judgeComplete(item)
        if result:
            item.pop('titles')
            yield item

    def judgeComplete(self,item):
        keys = item['titles']
        result: bool = True
        for key in keys :
            ret = key in item
            if False == ret:
                result = False
                break
        return result

from scrapy.cmdline import execute
import os
import sys
if __name__ == '__main__':

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy','crawl','illsets','-o','test1.jsonl'])
