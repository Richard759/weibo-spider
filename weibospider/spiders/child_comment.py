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
from items import ChildCommentItem
from spiders.utils import extract_comment_content, time_fix, get_create_time
from settings import CHILD_COMMENT_URL
import math
import datetime
from spiders.utils import id2mid, mid2id
import json


class ChildCommentSpider(Spider):
    name = "child_comment_spider"
    base_url = "https://weibo.com"

    def start_requests(self):
        child_urls = CHILD_COMMENT_URL  # 想要爬取的微博id，在weibo.com上找到相应微博，id就是url上的一串字符
        for child_url in child_urls:
            base_url = ('https://weibo.com/aj/v6/comment/big?ajwvr=6&' + child_url + '&from=singleWeiBo')
            yield Request(base_url, callback=self.parse)

    def parse(self, response):
        time.sleep(random.randint(3, 5))
        comment_weibo_id = id2mid(re.findall(r'&id=(.*?)&', response.url)[0])
        root_weibo_id = re.findall(r'&root_comment_id=(.*?)&', response.url)[0]
        tree_node = etree.HTML(str(json.loads(response.text)['data']))
        comment_nodes = tree_node.xpath('.//div[@class="list_li S_line1 clearfix"]')
        for comment_node in comment_nodes:
            try:
                comment_item = ChildCommentItem()
                comment_item['weibo_id'] = comment_weibo_id
                comment_item['root_comment_id'] = root_weibo_id
                comment_item['content'] = ''.join(
                    comment_node.xpath('./div[@class="list_con"]/div[@class="WB_text"]//text()')[2:]).replace(
                    '\n', "").replace('\r', "").replace(' ', "").replace(',', '，').strip()[1:]
                comment_item['_id'] = comment_node.xpath('./@comment_id')[0]
                comment_item['comment_user_id'] = ''.join(comment_node.xpath('./div[@class="list_con"]'
                                                                             '/div[@class="WB_text"]'
                                                                             '/a[1]/@usercard'))[3:]
                comment_item['comment_user'] = ''.join(comment_node.xpath('./div[@class="list_con"]'
                                                                          '/div[@class="WB_text"]/a[1]/text()'))
                info = ''.join(comment_node.xpath('./div[@class="list_con"]/div[@class="WB_func clearfix"]'
                                                  '/div[@class="WB_from S_txt2"]/text()'))
                comment_item['created_at'] = get_create_time(info)
                like_num = comment_node.xpath('.//a[@action-type="fl_like"]'
                                              '/span[@node-type="like_status"]/em[2]/text()')[0]
                if like_num == '赞':
                    comment_item['like_num'] = '0'
                else:
                    comment_item['like_num'] = like_num
                comment_item['crawl_time'] = int(time.time())
                yield comment_item
            except Exception as e:
                self.logger.error(e)
        try:
            next_page = ''.join(tree_node.xpath('.//a[@action-type="click_more_child_comment_big"]/@action-data'))
            page_url = ('https://weibo.com/aj/v6/comment/big?ajwvr=6&' + next_page + '&from=singleWeiBo')
            yield Request(page_url, callback=self.parse)
        except IndexError:
            return
