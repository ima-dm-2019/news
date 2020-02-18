# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from db_tools.tmt_dbm import TmtDBM


class NewsPipeline(object):
    def __init__(self):
        self.tmtdbm = TmtDBM()

    def process_item(self, item, spider):
        if spider.name == 'tmtSpider':
            record = []
            for key in ('url', 'title', 'publish_time', 'likes'):
                record.append(item[key])
            self.tmtdbm.dump_news(record)
        return item
