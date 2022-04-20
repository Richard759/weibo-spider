#!/usr/bin/env python
# encoding: utf-8

import datetime
import re
from lxml import etree
from scrapy import Spider
from scrapy.http import Request
from spiders.utils import get_create_time, extract_new_content
from settings import TWEET_DATE_WINDOW, TWEET_KEY_WORDS, CHOOSE_TYPE, CHOOSE_CONTAINS, MAX_DELTA
from items import TweetItem
import random
from time import sleep
import time



class TweetSpider(Spider):
    name = "tweet_spider"
    base_url = "https://s.weibo.com"

    def start_requests(self):

        def init_url_by_keywords():
            # crawl tweets include keywords in a period, you can change the following keywords and date
            keywords = TWEET_KEY_WORDS  # 按话题找微博，需要设置起止时间
            date_start = datetime.datetime.strptime(TWEET_DATE_WINDOW["start_date"], '%Y-%m-%d')
            date_end = datetime.datetime.strptime(TWEET_DATE_WINDOW["end_date"], '%Y-%m-%d')
            time_spread = datetime.timedelta(days=MAX_DELTA)
            url_format = ("https://s.weibo.com/weibo?q={}" + CHOOSE_TYPE + CHOOSE_CONTAINS + "&typeall=1&suball=1"
                          "&timescope=custom:{}:{}&Refer=g&page=1")
            # url_format = "https://s.weibo.com/weibo?q={}&timescope=custom:{}:{}&Refer=SWeibo_box&page=1"
            urls = []
            while date_start <= date_end:
                for keyword in keywords:
                    # 添加按日的url
                    keyword = keyword.replace('#', '%23')
                    day_string_end = date_end.strftime("%Y-%m-%d")
                    # day_string_start = date_end.strftime("%Y-%m-%d")
                    day_string_start = (date_end - datetime.timedelta(days=MAX_DELTA - 1)).strftime("%Y-%m-%d")
                    urls.append(url_format.format(keyword, day_string_start, day_string_end))
                date_end = date_end - time_spread
            url_set = list(set(urls))
            return url_set

        # select urls generation by the following code
        urls = init_url_by_keywords()
        # urls = init_url_by_user_id()
        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        sleep(random.randint(1, 3))
        tree_node = etree.HTML(response.body)
        # print(response.body)
        all_page = len(tree_node.xpath('//div[@class="m-page"]//ul[@class="s-scroll"]//li//a//text()'))
        start_date, end_date = re.findall(r'.*custom:(.*?):(.*?)&Refer=g.*', response.url)[0]
        if all_page == 50 and not ((len(start_date) == 12 or len(start_date) == 13) and start_date == end_date):
            if len(start_date) == 10:
                date_start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                date_end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                if (date_start - date_end).days == 0:
                    start_string = start_date + '-0'
                    end_string = start_date + '-11'
                    new_url_1 = re.sub(r'(custom):.*?(:.*?&Refer=g)', r'\1:%s\2' % start_string, response.url)
                    new_url_1 = re.sub(r'(custom:.*?):.*?(&Refer=g)', r'\1:%s\2' % end_string, new_url_1)
                    yield Request(new_url_1, callback=self.parse)
                    start_string = start_date + '-12'
                    end_string = start_date + '-23'
                    new_url_2 = re.sub(r'(custom):.*?(:.*?&Refer=g)', r'\1:%s\2' % start_string, response.url)
                    new_url_2 = re.sub(r'(custom:.*?):.*?(&Refer=g)', r'\1:%s\2' % end_string, new_url_2)
                    yield Request(new_url_2, callback=self.parse)
                else:
                    date_start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                    date_end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                    day_delta = (date_end - date_start).days + 1
                    new_date = date_end - datetime.timedelta(days=int(day_delta / 2))
                    day_string = new_date.strftime("%Y-%m-%d")
                    new_url_1 = re.sub(r'(custom:.*?):.*?(&Refer=g)', r'\1:%s\2' % day_string, response.url)
                    print(new_url_1)
                    yield Request(new_url_1, callback=self.parse)
                    day_string = (new_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                    new_url_2 = re.sub(r'(custom):.*?(:.*?&Refer=g)', r'\1:%s\2' % day_string, response.url)
                    yield Request(new_url_2, callback=self.parse)
            elif len(start_date) == 12 or len(start_date) == 13:
                date_start = datetime.datetime.strptime(start_date, '%Y-%m-%d-%H')
                date_end = datetime.datetime.strptime(end_date, '%Y-%m-%d-%H')
                # 2021-12-01-0:2021-12-01-3
                hour_delta = (date_end - date_start).seconds / 3600 + 1
                new_date = date_end - datetime.timedelta(hours=int(hour_delta / 2))
                day_string = new_date.strftime("%Y-%m-%d-%H")
                new_url_1 = re.sub(r'(custom:.*?):.*?(&Refer=g)', r'\1:%s\2' % day_string, response.url)
                yield Request(new_url_1, callback=self.parse)
                day_string = (new_date + datetime.timedelta(hours=1)).strftime("%Y-%m-%d-%H")
                new_url_2 = re.sub(r'(custom):.*?(:.*?&Refer=g)', r'\1:%s\2' % day_string, response.url)
                yield Request(new_url_2, callback=self.parse)
            else:
                print(start_date)
                raise KeyError
        else:
            if response.url.endswith('page=1'):
                sleep(random.randint(1, 3))
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse, dont_filter=True, meta=response.meta)
            try:
                tweet_nodes = tree_node.xpath('.//div[@class="card-wrap" and @action-type="feed_list_item"]')
                no_result = tree_node.xpath('.//div[@class="card card-no-result s-pt20b40"]')
                if no_result:
                    return
                for tweet_node in tweet_nodes:
                    tweet_item = TweetItem()
                    tweet_item['crawl_time'] = int(time.time())
                    original = tweet_node.xpath('.//div[@class="func"]/p[@class="from"]/a[1]/@href')  # 是否原创
                    tweet_item['image_count'] = len(tweet_node.xpath('.//ul/li/img/@src'))
                    tweet_item['image_url'] = '^'.join(tweet_node.xpath('.//ul/li/img/@src'))
                    tweet_item['repost_image_url'] = '^'.join(
                        tweet_node.xpath('.//div[@class="card-feed"]/div[@class="content"]'
                                         '/p[@node-type="feed_list_content"]/a[contains(text(),"查看图片")]/@href'))
                    tweet_item['video_url'] = ''.join(tweet_node.xpath(
                        './/div[@class="wbpv-contextmenu-address"]//text()')).strip()
                    if original:
                        tweet_item['origin_weibo'] = original[0]
                    weibo_url = ''.join(
                        tweet_node.xpath('.//div[@class="content"]/p[@class="from"]/a[1]/@href'))  # 微博URL
                    user_name = ''.join(tweet_node.xpath('.//div[@class="info"]/div/a[@class="name"]/text()'))
                    tweet_item['user_title'] = ''.join(tweet_node.xpath('.//div[@class="info"]'
                                                                        '/div/a[@target="_blank"]/i/@class'))
                    tweet_item['weibo_url'] = weibo_url
                    tweet_item['user_name'] = user_name.replace(',', '，')
                    try:
                        tweet_item['_id'] = re.findall(r'//weibo.com/\d+/(.*)\?refer_flag=.*', weibo_url)[0]  # 微博id
                        tweet_item['user_id'] = re.findall(r'//weibo.com/(\d+)/.*\?refer_flag=.*', weibo_url)[0]
                    except IndexError as e:
                        print("解析微博id出错啦！")
                    info = tweet_node.xpath('.//div[@class="content"]/p[@class="from"]/a[1]/text()')[-1].replace(
                        '\n', "").replace('\r', "").replace(' ', "")  # 微博发表时间
                    if info == '来自主持人的推荐':
                        info = tweet_node.xpath('.//div[@class="content"]/p[@class="from"]/a[2]/text()')[-1].replace(
                            '\n', "").replace('\r', "").replace(' ', "")  # 微博发表时间
                        tweet_item['tool'] = ''.join(tweet_node.xpath(
                            './/div[@class="content"]/p[@class="from"]/a[3]/text()')).replace('\n', "").replace(
                            '\r', "").replace(' ', "")
                    else:
                        tweet_item['tool'] = ''.join(tweet_node.xpath(
                            './/div[@class="content"]/p[@class="from"]/a[2]/text()')).replace('\n', "").replace(
                            '\r', "").replace(' ', "")
                    tweet_item['created_at'] = get_create_time(info)

                    try:
                        a_list = tweet_node.xpath('.//p[@class="txt"]/a')
                        local_info = ''
                        if len(a_list) > 0:
                            for i in a_list:
                                text_list = i.xpath('.//i/text()')
                                if len(text_list) > 0:
                                    text = text_list[0]
                                    if str(text) == '2':
                                        local_info = str(''.join(i.xpath('.//text()')))[1:]
                        tweet_item['location_map_info'] = local_info
                    except Exception as e:
                        print('获取位置出错了: ', e)
                    repost = tweet_node.xpath('.//div[@class="card"]/div[@class="card-act"]/ul/li[2]/a/text()')[
                        0].replace(
                        ' ', "")
                    comment = tweet_node.xpath('.//div[@class="card"]/div[@class="card-act"]/ul/li[3]/a/text()')[
                        0].replace(
                        ' ', "")
                    like = tweet_node.xpath('.//div[@class="card"]/div[@class="card-act"]/ul/li[4]/a/em/text()')
                    if like:
                        tweet_item['like_num'] = like[0]
                    else:
                        tweet_item['like_num'] = '0'
                    if repost[:2] == '转发' and len(repost) > 2:
                        tweet_item['repost_num'] = repost[2:]
                    else:
                        tweet_item['repost_num'] = '0'
                    if comment[:2] == '评论' and len(comment) > 2:
                        tweet_item['comment_num'] = comment[2:]
                    else:
                        tweet_item['comment_num'] = '0'
                    all_content_link = tweet_node.xpath('.//a[contains(@action-type,"fl_unfold")]')
                    repost_link = tweet_node.xpath('.//div[@node-type="feed_list_forwardContent"]')
                    if all_content_link:
                        if repost_link:
                            repost_more = tweet_node.xpath('.//div[@class="content"]/p[@node-type="feed_list_content"]'
                                                           '/a[contains(@action-type,"fl_unfold")]')
                            raw_more = tweet_node.xpath(
                                './/div[@node-type="feed_list_forwardContent"]/p[@node-type="feed_list_content"]'
                                '/a[contains(@action-type,"fl_unfold")]')
                            if repost_more:
                                base_row = tweet_node.xpath(
                                    './/div[@class="card-feed"]/div[@class="content"]'
                                    '/p[@node-type="feed_list_content_full"]')
                                content_raw = ''.join([etree.tostring(_, encoding='unicode') for _ in base_row])
                                repost_content = extract_new_content(content_raw)
                            else:
                                base_row = tweet_node.xpath(
                                    './/div[@class="card-feed"]/div[@class="content"]'
                                    '/p[@node-type="feed_list_content"]')
                                content_raw = ''.join([etree.tostring(_, encoding='unicode') for _ in base_row])
                                repost_content = extract_new_content(content_raw)
                            if raw_more:
                                base_row = tweet_node.xpath(
                                    './/div[@node-type="feed_list_forwardContent"]'
                                    '/p[@node-type="feed_list_content_full"]')
                                content_raw = ''.join([etree.tostring(_, encoding='unicode') for _ in base_row])
                                raw_content = extract_new_content(content_raw)
                            else:
                                base_row = tweet_node.xpath(
                                    './/div[@node-type="feed_list_forwardContent"]'
                                    '/p[@node-type="feed_list_content"]')
                                content_raw = ''.join([etree.tostring(_, encoding='unicode') for _ in base_row])
                                raw_content = extract_new_content(content_raw)
                            tweet_item['content'] = f'转发理由：{repost_content}//{raw_content}'
                        else:
                            base_row = tweet_node.xpath(
                                './/div[@class="content"]/p[@node-type="feed_list_content_full"]')
                            content_raw = ''.join([etree.tostring(_, encoding='unicode') for _ in base_row])
                            tweet_item['content'] = extract_new_content(content_raw)
                    elif repost_link:
                        base_row = tweet_node.xpath(
                            './/div[@class="card-feed"]/div[@class="content"]'
                            '/p[@node-type="feed_list_content"]')
                        content_raw = ''.join([etree.tostring(_, encoding='unicode') for _ in base_row])
                        repost_content = extract_new_content(content_raw)

                        base_row = tweet_node.xpath(
                            './/div[@node-type="feed_list_forwardContent"]'
                            '/p[@node-type="feed_list_content"]')
                        content_raw = ''.join([etree.tostring(_, encoding='unicode') for _ in base_row])
                        raw_content = extract_new_content(content_raw)
                        tweet_item['content'] = f'转发理由：{repost_content}//{raw_content}'
                    else:
                        base_row = tweet_node.xpath(
                            './/div[@class="content"]/p[@node-type="feed_list_content"]')
                        content_raw = ''.join([etree.tostring(_, encoding='unicode') for _ in base_row])
                        tweet_item['content'] = extract_new_content(content_raw)
                    yield tweet_item
            except Exception as e:
                print('解析微博信息出错啦:', e)
