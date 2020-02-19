# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from db_tools.tmt_dbm import TmtDBM
from db_tools.kr_dbm import KrDBM
from db_tools.hx_dbm import HxDBM

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


class KrPipeline(object):
    def __init__(self):
        self.krdbm = KrDBM()

    def process_item(self, item, spider):
        if spider.name == 'krSpider':
            record = []
            for key in ('url', 'title', 'description', 'publish_time', 'username'):
                record.append(item[key])
            self.krdbm.dump_news(record)
        return item

class HxPipeline(object):
    def __init__(self):
        self.hxdbm = HxDBM()

    def process_item(self, item, spider):
        if spider.name == 'hxSpider':
            news_record = []
            # 新闻信息
            for key in ('url', 'title', 'description', 'publish_time', 'username', 'user_id', 'agree_number',
                        'favorite_number', 'video_url'):
                news_record.append(item[key])
            news_record.append(str(item['comment_list']))
            self.hxdbm.dump_news(news_record)
            # 用户信息
            user_record = []
            for key in ('username', 'user_id', 'avatar', 'url', 'one_word'):
                user_record.append(item[key])
            self.hxdbm.dump_users(user_record)
            # 评论信息
            for comment_info in item['comment_info_list']:
                comment_record = []
                for key in ('comment_id', 'username', 'user_id', 'content', 'publish_time',
                            'agree_number', 'disagree_number'):
                    comment_record.append(comment_info[key])
                self.hxdbm.dump_comment(comment_record)
                user_record = []
                # 评论中用户信息
                for key in ('username', 'user_id', 'avatar', 'url', 'one_word'):
                    user_record.append(comment_info[key])
                self.hxdbm.dump_users(user_record)
        return item
