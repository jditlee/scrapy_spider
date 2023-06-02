# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IllItem(scrapy.Item):
    # define the fields for your item here like:
    ill_name = scrapy.Field() # 疾病名称
    addr = scrapy.Field() # 地址
    intro = scrapy.Field() # 简介
    ill_part = scrapy.Field() # 发病部位
    ill_dep = scrapy.Field() # 就诊科室
    ill_med = scrapy.Field() # 疾病用药
    ill_self_test = scrapy.Field() # 疾病自测
    ill_other_addr = scrapy.Field() # 其它地址
    ill_desc = scrapy.Field() # 疾病介绍
    ill_cause = scrapy.Field() # 病因
    ill_symptom = scrapy.Field() # 症状
    ill_check = scrapy.Field() # 检查
    ill_prevent = scrapy.Field() # 预防
    ill_cure = scrapy.Field() # 治疗
    ill_identify = scrapy.Field() # 鉴别
    ill_complication = scrapy.Field() # 并发症

class YanXuanItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    times = scrapy.Field()  # 标题
    content = scrapy.Field()  # 内容
    types = scrapy.Field()  # 类别
    href = scrapy.Field()  # 链接
