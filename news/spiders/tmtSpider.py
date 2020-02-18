# -*- coding: utf-8 -*-
from scrapy import Spider, Selector, Request
import datetime


class TmtspiderSpider(Spider):
    name = 'tmtSpider'
    allowed_domains = ['tmtpost.com']
    start_urls = ['https://www.tmtpost.com/nictation/']
    cur_date = datetime.date.today().strftime('%Y%m%d')

    def parse(self, response):
        selector = Selector(text=response.text)
        eroot = selector.xpath('/html/body/div/section/div/div')
        date_ = eroot.xpath('./div/time/text()').extract_first()
        date_ = date_[:4] + date_[5:7] + date_[8:10]
        if date_ != TmtspiderSpider.cur_date:
            return
        word_list = eroot.xpath('./ul')
        if len(word_list) == 2:
            word_list, page_list = eroot.xpath('./ul')
            for page in page_list.xpath('./li'):
                url = page.xpath('./a/@href').extract_first()
                if url is not None:
                    yield Request(url, callback=self.parse, dont_filter=False)
        # 标题信息
        for word in word_list.xpath('./li'):
            info = {}
            info['url'] = word.xpath('./h2/a/@href').extract_first()
            info['title'] = word.xpath('./h2/a/text()').extract_first()
            info['publish_time'] = word.xpath('./div/time/text()').extract_first()
            info['likes'] = word.xpath('./div/div/span[2]/span/text()').extract_first()
            yield info
