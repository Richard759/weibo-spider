#!/usr/bin/env python
# encoding: utf-8
"""
File Description: 
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2020/4/14
"""
import datetime
import re
from lxml import etree
from scrapy import Spider
from scrapy.http import Request
import time
from settings import TWEET_DATE_WINDOW, TWEET_KEY_WORDS
from items import TweetItem
from spiders.utils import time_fix, extract_weibo_content
import random
import pandas as pd
import csv
from time import sleep
import time


class TweetSpider(Spider):
    name = "tweet_spider"
    base_url = "https://s.weibo.com"

    def start_requests(self):

        def init_url_by_user_id():
            # crawl specific users' tweets in a specific date
            # === change the following config ===
            user_ids = ['1618051664',  # 头条新闻
                        '1314608344',  # 新闻晨报
                        '2656274875',  # 央视新闻
                        '1496814565',  # 封面新闻
                        '2028810631',  # 新浪新闻
                        '5044281310',  # 澎湃新闻
                        '1784473157',  # 中国新闻网
                        '1644114654',  # 新京报
                        '2615417307',  # 凤凰网
                        '2810373291']  # 新华网
            # === change the above config ===
            start_date = datetime.datetime.strptime("2017-01-01", '%Y-%m-%d')
            end_date = datetime.datetime.strptime("2021-11-22", '%Y-%m-%d')
            # === change the above config ===
            time_spread = datetime.timedelta(days=5)
            # url_format_hash = ("https://weibo.cn/{}/profile?hasori=0&haspic=0&"
            #                    "starttime={}&endtime={}&advancedfilter=1&page=1")

            url_format = "https://weibo.cn/{}/profile?hasori=0&haspic=0&starttime={}&endtime={}&advancedfilter=1&page=1"
            urls = []
            while start_date < end_date:
                for user_id in user_ids:
                    start_date_string = start_date.strftime("%Y%m%d")
                    tmp_end_date = start_date + time_spread
                    if tmp_end_date >= end_date:
                        tmp_end_date = end_date
                    end_date_string = tmp_end_date.strftime("%Y%m%d")
                    urls.append(url_format.format(user_id, start_date_string, end_date_string))
                start_date = start_date + time_spread
            return urls

        def init_url_by_keywords():
            # crawl tweets include keywords in a period, you can change the following keywords and date
            keywords = TWEET_KEY_WORDS  # 按话题找微博，需要设置起止时间
            date_start = datetime.datetime.strptime(TWEET_DATE_WINDOW["start_date"], '%Y-%m-%d')
            date_end = datetime.datetime.strptime(TWEET_DATE_WINDOW["end_date"], '%Y-%m-%d')
            time_spread = datetime.timedelta(days=1)
            url_format = "https://s.weibo.com/weibo?q={}&typeall=1&suball=1&timescope=custom:{}:{}&Refer=g&page=1"
            # url_format = "https://s.weibo.com/weibo?q={}&timescope=custom:{}:{}&Refer=SWeibo_box&page=1"
            urls = []
            while date_start <= date_end:
                for keyword in keywords:
                    # 添加按日的url
                    keyword = keyword.replace('#', '%23')
                    day_string_end = date_end.strftime("%Y-%m-%d")
                    day_string_start = date_end.strftime("%Y-%m-%d")
                    # day_string_start = (date_end - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                    urls.append(url_format.format(keyword, day_string_start, day_string_end))
                date_end = date_end - time_spread
            url_set = list(set(urls))
            return url_set

        # select urls generation by the following code
        urls = init_url_by_keywords()
        # urls = init_url_by_user_id()
        # headers1 = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50',
        #     'Cookie': 'SINAGLOBAL=2984020340573.4653.1615966504509; _s_tentry=-; Apache=5630874165587.54.1635862344926; ULV=1635862344931:36:1:1:5630874165587.54.1635862344926:1635506938379; login_sid_t=dfd0374e19e48765b13a3f1dc35d0411; cross_origin_proto=SSL; ALF=1667398812; SSOLoginState=1635862812; SCF=At9eOLw9o69sap1_tTXMdkUPPcB7_jux_87EDPewfgITu_-_9z6hMrNwlH0yLZETYTrbqNmn59eMMulcI1cMzpw.; SUB=_2A25MhTlMDeRhGeBL7VsU8SzJzjyIHXVv8y2ErDV8PUNbmtANLRH-kW9NRvFrV3mcz6UXhpp05hlURS8mzibI4IqI; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh5h_i4eSgoD7jFisEd1k8Y5JpX5KzhUgL.FoqfSo.feKzfSK52dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcSKq4SK2ESK-7; wvr=6; UOR=,,login.sina.com.cn; webim_unReadCount=%7B%22time%22%3A1635864936064%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A42%2C%22msgbox%22%3A0%7D'}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44',
            'Cookie': 'SINAGLOBAL=2984020340573.4653.1615966504509; UOR=,,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh5h_i4eSgoD7jFisEd1k8Y5JpX5KMhUgL.FoqfSo.feKzfSK52dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcSKq4SK2ESK-7; ALF=1669021847; SSOLoginState=1637485848; SCF=At9eOLw9o69sap1_tTXMdkUPPcB7_jux_87EDPewfgITZPhZfmOC0h1ApQf7JN1bBNDGhNePUbPRdlM2aeHaoXA.; SUB=_2A25Mnn1IDeRhGeBL7VsU8SzJzjyIHXVv6umArDV8PUNbmtB-LUn9kW9NRvFrV0ZBgLK1SIj5SA3G6hgzugm1SYvS; wvr=6; _s_tentry=-; Apache=3679075520440.2803.1637485851733; ULV=1637485851738:41:6:1:3679075520440.2803.1637485851733:1636733787083; webim_unReadCount=%7B%22time%22%3A1637485866279%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A40%2C%22msgbox%22%3A0%7D; WBStorage=5fd44921|undefined'}
        headers2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44',
            'Cookie': 'SINAGLOBAL=2984020340573.4653.1615966504509; UOR=,,login.sina.com.cn; webim_unReadCount=%7B%22time%22%3A1636725673060%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A42%2C%22msgbox%22%3A0%7D; _s_tentry=login.sina.com.cn; Apache=2903802932720.7427.1636733787078; ULV=1636733787083:40:5:3:2903802932720.7427.1636733787078:1636725696399; WBStorage=5fd44921|undefined; login_sid_t=7de44892f656f3a956f56941a326cc83; cross_origin_proto=SSL; ALF=1668270078; SSOLoginState=1636734079; SCF=At9eOLw9o69sap1_tTXMdkUPPcB7_jux_87EDPewfgIT--SQlP57nGxTu7hOoBn2GTz39S1SjYf6QfokkKQMRn0.; SUB=_2A25MiuQuDeRhGeBL7VsU8SzJzjyIHXVv_lLmrDV8PUNbmtB-LRPSkW9NRvFrVzTwlK5mqNvLS5zWZzRRuBNJljoI; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh5h_i4eSgoD7jFisEd1k8Y5JpX5KzhUgL.FoqfSo.feKzfSK52dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcSKq4SK2ESK-7; wvr=6'}
        for url in urls:
            yield Request(url, callback=self.parse)
            # if int(time.time()) % 3 == 0:
            #     yield Request(url, callback=self.parse, headers=headers2)
            # else:
            #     yield Request(url, callback=self.parse, headers=headers1)

    def parse(self, response):
        sleep(random.randint(1, 3))
        tree_node = etree.HTML(response.body)
        # print(response.body)
        if response.url.endswith('page=1'):
            sleep(random.randint(1, 3))
            all_page = len(tree_node.xpath('//div[@class="m-page"]//ul[@class="s-scroll"]//li//a//text()'))
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
                # print(original)
                # df = pd.read_csv('weiboid.csv', encoding='utf-8-sig')
                # weibo_id_list = df['weibo_id'].tolist()
                if original:
                    tweet_item['origin_weibo'] = original[0]
                weibo_url = ''.join(tweet_node.xpath('.//div[@class="content"]/p[@class="from"]/a[1]/@href'))  # 微博URL
                tweet_item['weibo_url'] = weibo_url
                try:
                    tweet_item['_id'] = re.findall(r'//weibo.com/\d+/(.*)\?refer_flag=.*', weibo_url)[0]  # 微博id
                    tweet_item['user_id'] = re.findall(r'//weibo.com/(\d+)/.*\?refer_flag=.*', weibo_url)[0]
                except IndexError as e:
                    print("解析微博id出错啦！")
                tweet_item['tool'] = ''.join(tweet_node.xpath(
                    './/div[@class="content"]/p[@class="from"]/a[2]/text()')).replace('\n', "").replace(
                    '\r', "").replace(' ', "")
                info = tweet_node.xpath('.//div[@class="content"]/p[@class="from"]/a[1]/text()')[-1].replace(
                    '\n', "").replace('\r', "").replace(' ', "")  # 微博发表时间
                if re.match(r'^20..年..月..日.*', info):
                    time_index = f'{info[0:4]}-{info[5:7]}-{info[8:10]} {info[11:]}'
                elif re.match(r'^..月..日.*', info):
                    time_index = f'2021-{info[0:2]}-{info[3:5]} {info[6:]}'
                elif re.match(r'^今天.*', info):
                    time_index = f'{datetime.date.today()} {info[2:]}'
                else:
                    time_index = info
                tweet_item['created_at'] = time_index
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
                repost = tweet_node.xpath('.//div[@class="card"]/div[@class="card-act"]/ul/li[2]/a/text()')[0].replace(
                    ' ', "")
                comment = tweet_node.xpath('.//div[@class="card"]/div[@class="card-act"]/ul/li[3]/a/text()')[0].replace(
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
                print(like, repost, comment)
                all_content_link = tweet_node.xpath('.//a[text()="展开全文" and contains(@action-type,"fl_unfold")]')
                repost_link = tweet_node.xpath('.//div[@node-type="feed_list_forwardContent"]')
                if all_content_link:
                    if repost_link:
                        repost_more = tweet_node.xpath('.//div[@class="content"]/p[@node-type="feed_list_content"]'
                                                       '/a[text()="展开全文" and contains(@action-type,"fl_unfold")]')
                        raw_more = tweet_node.xpath(
                            './/div[@node-type="feed_list_forwardContent"]/p[@node-type="feed_list_content"]'
                            '/a[text()="展开全文" and contains(@action-type,"fl_unfold")]')
                        if repost_more:
                            repost_content = ''.join(tweet_node.xpath(
                                './/div[@class="card-feed"]/div[@class="content"]'
                                '/p[@node-type="feed_list_content_full"]//text()')).replace(
                                '\n', "").replace('\r', "").replace(' ', "")[:-5]
                        else:
                            repost_content = ''.join(tweet_node.xpath(
                                './/div[@class="card-feed"]/div[@class="content"]'
                                '/p[@node-type="feed_list_content"]//text()')).replace(
                                '\n', "").replace('\r', "").replace(' ', "")
                        if raw_more:
                            raw_content = ''.join(tweet_node.xpath(
                                './/div[@node-type="feed_list_forwardContent"]'
                                '/p[@node-type="feed_list_content_full"]//text()')).replace(
                                '\n', "").replace('\r', "").replace(' ', "")[:-5]
                        else:
                            raw_content = ''.join(tweet_node.xpath(
                                './/div[@node-type="feed_list_forwardContent"]'
                                '/p[@node-type="feed_list_content"]//text()')).replace(
                                '\n', "").replace('\r', "").replace(' ', "")
                        tweet_item['content'] = f'转发理由：{repost_content}//{raw_content}'
                    else:
                        tweet_item['content'] = ''.join(tweet_node.xpath(
                            './/div[@class="content"]/p[@node-type="feed_list_content_full"]//text()')).replace(
                            '\n', "").replace('\r', "").replace(' ', "")[:-5]
                elif repost_link:
                    repost_content = ''.join(tweet_node.xpath(
                        './/div[@class="card-feed"]/div[@class="content"]'
                        '/p[@node-type="feed_list_content"]//text()')).replace(
                        '\n', "").replace('\r', "").replace(' ', "")
                    raw_content = ''.join(tweet_node.xpath(
                        './/div[@node-type="feed_list_forwardContent"]'
                        '/p[@node-type="feed_list_content"]//text()')).replace(
                        '\n', "").replace('\r', "").replace(' ', "")[:-5]
                    tweet_item['content'] = f'转发理由：{repost_content}//{raw_content}'
                else:
                    tweet_item['content'] = ''.join(tweet_node.xpath(
                        './/div[@class="content"]/p[@node-type="feed_list_content"]//text()')).replace(
                        '\n', "").replace('\r', "").replace(' ', "")  # 微博内容
                yield tweet_item
        except Exception as e:
            print('解析微博信息出错啦:', e)