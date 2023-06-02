# -*- coding:utf-8 -*-
# author:凌陨心
# datetime:2023/5/16 11:10
# software: PyCharm
from scrapy import cmdline
cmdline.execute('scrapy crawl yanxuan'.split())

# cmdline.execute('scrapy crawl ill_craw'.split())
# cmdline.execute('scrapy crawl illsets -o data/tnb.jsonl'.split())
# cmdline.execute('scrapy crawl ill_craw -o data/all_ill.csv'.split())
# cmdline.execute('scrapy crawl ill_craw -o data/all_ill.jsonl'.split())

# cmdline.execute('scrapy crawl sina_spider'.split())