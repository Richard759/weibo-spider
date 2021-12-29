#!/usr/bin/env python
# encoding: utf-8
"""
File Description: 
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2019-12-07 21:27
"""
import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.tweet import TweetSpider
from spiders.comment import CommentSpider
from spiders.follower import FollowerSpider
from spiders.user import UserSpider
from spiders.fan import FanSpider
from spiders.repost import RepostSpider
from spiders.user_brief import UserBriefSpider

mode = sys.argv[1]

if __name__ == '__main__':
    os.environ['SCRAPY_SETTINGS_MODULE'] = f'settings'
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    mode_to_spider = {
        'comment': CommentSpider,
        'fan': FanSpider,
        'follow': FollowerSpider,
        'tweet': TweetSpider,
        'user': UserSpider,
        'repost': RepostSpider,
        'user_brief': UserBriefSpider
    }
    process.crawl(mode_to_spider[mode])
    # the script will block here until the crawling is finished
    process.start()
