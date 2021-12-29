#!/usr/bin/env python
# encoding: utf-8

import re
from scrapy import Selector, Spider
from scrapy.http import Request
import time
from items import UserBriefItem
from settings import USER_ID


def get_weibo_num(string):
    if string[-1] == '万':
        return int(float(string[:-1]) * 10000)
    elif string[-1] == '亿':
        return int(float(string[:-1]) * 100000000)
    else:
        return int(string)


class UserBriefSpider(Spider):
    name = "user_brief_spider"
    base_url = "https://weibo.cn"

    def start_requests(self):
        user_ids = USER_ID
        urls = [f'{self.base_url}/u/{user_id}' for user_id in user_ids]
        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        time.sleep(0.5)
        user_item = UserBriefItem()
        user_item['crawl_time'] = int(time.time())
        text = response.text
        user_item['_id'] = re.findall(r'/u/(\d+)', response.url)[0]
        tweets_num = re.findall(r'微博\[(.*?)\]', text)
        user_item['tweets_num'] = get_weibo_num(tweets_num[0])
        follows_num = re.findall(r'关注\[(.*?)\]', text)
        user_item['follows_num'] = get_weibo_num(follows_num[0])
        fans_num = re.findall(r'粉丝\[(.*?)\]', text)
        user_item['fans_num'] = get_weibo_num(fans_num[0])
        yield user_item
