# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from .dao.mongo_db import MongoDB

class IllPipeline:
    """
    写入mongoDB
    """
    def __init__(self):
        self.mongo = MongoDB(db='scrapy_data')
        self.collection = self.mongo.db_scrapy['ill_ori_drop_duplicate'] # 疾病数据

    def process_item(self, item, spider):
        result_item = dict(item)
        self.collection.insert_one(result_item)
        return item

class YanXuanPipeline:
    """
    写入mongoDB
    """
    def __init__(self):
        self.mongo = MongoDB(db='scrapy_data')
        # self.collection = self.mongo.db_scrapy['yan_xuan_ori'] # 盐选数据
        self.collection = self.mongo.db_scrapy['yan_xuan_ori_new'] # 盐选数据

    def process_item(self, item, spider):
        result_item = dict(item)
        self.collection.insert_one(result_item)
        return item

class DropDuplicatePipeline:
    """
    过滤重复数据
    """
    def __init__(self):
        self.name_dict = set()
    def process_item(self, item, spider):
        name = item['ill_name'].strip()
        if name in self.name_dict:
            raise DropItem("drop duplicate ill %s" % name)
        self.name_dict.add(name)
        return item