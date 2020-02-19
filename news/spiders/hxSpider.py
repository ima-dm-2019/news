# -*- coding: utf-8 -*-
from scrapy import Selector, Spider, FormRequest
import json, re, datetime, time

class HxspiderSpider(Spider):
    name = 'hxSpider'
    allowed_domains = ['huxiu.com/moment', 'moment-api.huxiu.com']
    start_urls = ['https://www.huxiu.com/moment/']
    today = time.mktime(datetime.date.today().today().timetuple())

    def parse(self, response):
        selector = Selector(response=response)
        data_text = selector.xpath('*//script').extract_first()
        if data_text:
            data_str = re.findall('{.*};', data_text)[0]
            data = json.loads(data_str[:-1])
            moment = data['moment']
            moment_list = moment['momentList']['moment_list']
            news_list = moment_list['datalist'][0]['datalist']  # 今天的新闻
            last_dateline = moment_list['last_dateline']
            if last_dateline >= HxspiderSpider.today:
                form_data = {'last_dateline': str(last_dateline), 'platform': 'www', 'is_ai': '0'}
                yield FormRequest(url='https://moment-api.huxiu.com/web-v2/moment/feed', formdata=form_data,
                                  callback=self.next_page)
            for news in news_list:
                info = {}
                # 新闻信息
                info['url'] = news['url']
                title_description = news['content'].split('<br><br>', 1)
                if len(title_description) == 2:
                    info['title'] = title_description[0]
                    info['description'] = title_description[1]
                else:
                    info['title'] = ''
                    info['description'] = title_description[0]

                info['publish_time'] = time.strftime('%H:%M:%S', time.localtime(int(news['publish_time'])))
                info['agree_number'] = news['agree_num']
                info['favorite_number'] = news['favorite_num']
                info['video_url'] = ''
                if 'video' in news.keys():
                    info['video_url'] = news['video']['url']

                # 用户信息
                user_info = news['user_info']
                info['username'] = user_info['username']
                info['user_id'] = user_info['uid']
                info['avatar'] = user_info['avatar']
                info['url'] = f'https://www.huxiu.com/member/{user_info["uid"]}/moment.html'
                info['one_word'] = user_info['yijuhua']

                # 评论信息
                comment_info_list = []
                comment_id_list = []
                for comment_info in news['comment']['datalist']:
                    c_info = {}
                    comment_id_list.append(comment_info['comment_id'])
                    c_info['comment_id'] = comment_info['comment_id']
                    c_info['content'] = comment_info['content']
                    c_info['publish_time'] = time.strftime('%H:%M:%S', time.localtime(int(comment_info['time'])))
                    c_info['disagree_number'] = comment_info['disagree_num']
                    c_info['agree_number'] = comment_info['agree_num']
                    comment_info_list.append(c_info)
                    # 评论中的用户信息
                    user_info = comment_info['user_info']
                    c_info['username'] = user_info['username']
                    c_info['user_id'] = user_info['uid']
                    c_info['avatar'] = user_info['avatar']
                    c_info['one_word'] = user_info.get('yijuhua', '')  # 评论用户无此字段
                    c_info['url'] = f'https://www.huxiu.com/member/{user_info["uid"]}/comment'
                info['comment_list'] = comment_id_list
                info['comment_info_list'] = comment_info_list
                yield info

    def next_page(self, response):
        data = json.loads(response.text)
        moment_list = data['data']['moment_list']  # moment
        news_list = moment_list['datalist'][0]['datalist']  # 今天的新闻
        last_dateline = moment_list['last_dateline']
        if last_dateline >= HxspiderSpider.today:
            form_data = {'last_dateline': str(last_dateline), 'platform': 'www', 'is_ai': '0'}
            yield FormRequest(url='https://moment-api.huxiu.com/web-v2/moment/feed', formdata=form_data,
                              callback=self.next_page)
        for news in news_list:
            info = {}
            # 新闻信息
            info['url'] = news['url']
            title_description = news['content'].split('<br><br>', 1)
            if len(title_description) == 2:
                info['title'] = title_description[0]
                info['description'] = title_description[1]
            else:
                info['title'] = ''
                info['description'] = title_description[0]

            info['publish_time'] = time.strftime('%H:%M:%S', time.localtime(int(news['publish_time'])))
            info['agree_number'] = news['agree_num']
            info['favorite_number'] = news['favorite_num']
            info['video_url'] = ''
            if 'video' in news.keys():
                info['video_url'] = news['video']['url']

            # 用户信息
            user_info = news['user_info']
            info['username'] = user_info['username']
            info['user_id'] = user_info['uid']
            info['avatar'] = user_info['avatar']
            info['url'] = f'https://www.huxiu.com/member/{user_info["uid"]}/moment.html'
            info['one_word'] = user_info['yijuhua']

            # 评论信息
            comment_info_list = []
            comment_id_list = []
            for comment_info in news['comment']['datalist']:
                c_info = {}
                comment_id_list.append(comment_info['comment_id'])
                c_info['comment_id'] = comment_info['comment_id']
                c_info['content'] = comment_info['content']
                c_info['publish_time'] = time.strftime('%H:%M:%S', time.localtime(int(comment_info['time'])))
                c_info['disagree_number'] = comment_info['disagree_num']
                c_info['agree_number'] = comment_info['agree_num']
                comment_info_list.append(c_info)
                # 评论中的用户信息
                user_info = comment_info['user_info']
                c_info['username'] = user_info['username']
                c_info['user_id'] = user_info['uid']
                c_info['avatar'] = user_info['avatar']
                c_info['one_word'] = user_info.get('yijuhua', '')  # 评论用户无此字段
                c_info['url'] = f'https://www.huxiu.com/member/{user_info["uid"]}/comment'
            info['comment_list'] = comment_id_list
            info['comment_info_list'] = comment_info_list
            yield info
