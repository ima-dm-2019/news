# -*- coding: utf-8 -*-
from scrapy import Spider, Selector, Request
import re, json, datetime


class KrspiderSpider(Spider):
    name = 'krSpider'
    allowed_domains = []#['36kr.com/newsflashes', '36kr.com/pp/api/newsflash']
    start_urls = ['http://36kr.com/newsflashes/']
    cur_date = datetime.date.today().strftime('%Y-%m-%d')

    def parse(self, response):
        selector = Selector(response=response)
        data_text = ''  # 要抓取的信息
        elems = selector.xpath('//script')
        for i, elem in enumerate(elems):
            text = elem.xpath('./text()').extract_first()
            if text:
                if text[:6] == 'window':
                    data_text = text
                    break
        if data_text:
            mouth = selector.xpath(
                '//*[@id="app"]/div/div[1]/div[3]/div/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/span[1]/text()')\
                .extract_first()
            day = selector.xpath(
                '//*[@id="app"]/div/div[1]/div[3]/div/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/span[2]/text()')\
                .extract_first()
            data = json.loads(re.findall('{.*}', data_text)[0])
            newsflash_catalog_data = data['newsflashCatalogData']['data']
            newsflash_list = newsflash_catalog_data['newsflashList']['data']
            for newsflash in newsflash_list:
                info = {}
                info['title'] = newsflash['title']
                info['description'] = newsflash['description']
                info['publish_time'] = newsflash['published_at']
                info['url'] = newsflash['news_url']
                info['username'] = newsflash['user']['name']
                yield info
            last_id = newsflash_list[-1]['id']
            url = f'https://36kr.com/pp/api/newsflash?b_id={last_id}&per_page=20'
            yield Request(url, callback=self.next_page)

    def next_page(self, response):
        items = json.loads(response.text)['data']['items']
        for item in items:
            if item['published_at'][:10] != KrspiderSpider.cur_date:
                return
            info = {}
            info['title'] = item['title']
            info['description'] = item['description']
            info['publish_time'] = item['published_at']
            info['url'] = item['news_url']
            info['username'] = item['user']['name']
            yield info
        last_id = items[-1]['id']
        url = f'https://36kr.com/pp/api/newsflash?b_id={last_id}&per_page=20'
        yield Request(url, callback=self.next_page)



