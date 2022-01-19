#!/usr/bin/env python
# encoding: utf-8
"""
File Description: 
Author: Richard
Mail: lingzhi_qi@163.com
Created Time: 2021-01-18
"""
import re
from lxml import etree
from scrapy import Spider
from scrapy.http import Request
import time
import random
from items import CommentItem
from spiders.utils import id2mid, mid2id
from settings import COMMENT_TWEET_ID
import datetime
import json


class CommentSpider(Spider):
    name = "comment_spider"
    base_url = "https://weibo.com"

    def start_requests(self):
        tweet_ids = COMMENT_TWEET_ID  # 想要爬取的微博id，在weibo.com上找到相应微博，id就是url上的一串字符
        for tweet_id in tweet_ids:
            base_url = ('https://weibo.com/aj/v6/comment/big?ajwvr=6&id=' + mid2id(tweet_id) +
                        '&root_comment_max_id_type=0&' + 'root_comment_ext_param=&page=1&from=singleWeiBo')
            # '&__rnd=' + str(int(time.time() * 1000)))
            yield Request(base_url, callback=self.parse)

    def parse(self, response):
        time.sleep(random.randint(3, 5))
        comment_weibo_id = id2mid(re.findall(r'&id=(.*?)&', response.url)[0])
        tree_node = etree.HTML(str(json.loads(response.text)['data']))
        tweet_nodes = tree_node.xpath('.//div[@node-type = "root_comment"]')
        for tweet_node in tweet_nodes:
            try:
                comment_item = CommentItem()
                comment_item['weibo_id'] = comment_weibo_id
                comment_item['content'] = ''.join(
                    tweet_node.xpath('./div[@class="list_con"]/div[@class="WB_text"]/text()[2]')).replace(
                    '\n', "").replace('\r', "").replace(' ', "").replace(',', '，')[1:]
                comment_item['_id'] = tweet_node.xpath('./@comment_id')[0]
                comment_item['comment_user_id'] = ''.join(tweet_node.xpath('./div[@class="list_con"]'
                                                                           '/div[@class="WB_text"]/a[1]/@usercard'))[3:]
                comment_item['comment_user'] = ''.join(tweet_node.xpath('./div[@class="list_con"]'
                                                                        '/div[@class="WB_text"]/a[1]/text()'))
                info = ''.join(tweet_node.xpath('./div[@class="list_con"]/div[@class="WB_func clearfix"]'
                                                '/div[@class="WB_from S_txt2"]/text()'))
                if re.match(r'^20..年..月..日.*', info):
                    time_index = f'{info[0:4]}-{info[5:7]}-{info[8:10]} {info[11:]}'
                elif re.match(r'^..月..日.*', info):
                    time_index = f'{datetime.date.today().year}-{info[0:2]}-{info[3:5]} {info[6:]}'
                elif re.match(r'^今天.*', info):
                    time_index = f'{datetime.date.today()} {info[2:]}'
                else:
                    time_index = info
                comment_item['created_at'] = time_index
                like_num = tweet_node.xpath('.//a[@action-type="fl_like"]'
                                            '/span[@node-type="like_status"]/em[2]/text()')[0]
                if like_num == '赞':
                    comment_item['like_num'] = '0'
                else:
                    comment_item['like_num'] = like_num
                comment_item['child_url'] = ''.join(tweet_node.xpath('.//a[@action-type="click_more_child_comment_big"]'
                                                                     '/@action-data'))
                comment_item['crawl_time'] = int(time.time())
                yield comment_item
            except Exception as e:
                self.logger.error(e)
        try:
            next_page = tree_node.xpath('.//div[@node-type="comment_loading"]/@action-data')[0]
        except IndexError:
            try:
                next_page = tree_node.xpath('.//a[@action-type="click_more_comment"]/@action-data')[0]
            except IndexError:
                return
        page_url = ('https://weibo.com/aj/v6/comment/big?ajwvr=6&' + next_page + '&from=singleWeiBo')
        yield Request(page_url, callback=self.parse)
