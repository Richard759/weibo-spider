import datetime
import re
from lxml import etree
from scrapy import Spider
from scrapy.http import Request
import time
import random
from items import TweetItem
from urllib.parse import unquote
from spiders.utils import time_fix, extract_weibo_content
from settings import USER_TWEET_ID, TWEET_DATE_WINDOW


class UserTweetSpider(Spider):
    name = "user_tweet_spider"
    base_url = "https://weibo.cn"

    def start_requests(self):

        def init_url_by_user_id_and_date():
            user_ids = USER_TWEET_ID
            start_date = datetime.datetime.strptime(TWEET_DATE_WINDOW["start_date"], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(TWEET_DATE_WINDOW["end_date"], '%Y-%m-%d')
            # === change the above config ===
            time_spread = datetime.timedelta(days=10)
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

        # select urls generation by the following code
        # urls = init_url_by_user_id()
        # urls = init_url_by_keywords_and_date()
        urls = init_url_by_user_id_and_date()
        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        time.sleep(random.uniform(3, 5))
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                start_date, end_date = re.findall(r'.*starttime=(.*)&endtime=(.*)&advancedfilter.*', response.url)[0]
                if all_page > 80 and start_date != end_date:
                    date_start = datetime.datetime.strptime(start_date, '%Y%m%d')
                    date_end = datetime.datetime.strptime(end_date, '%Y%m%d')
                    day_delta = (date_end - date_start).days + 1
                    new_date = date_end - datetime.timedelta(days=int(day_delta / 2))
                    day_string = new_date.strftime("%Y%m%d")
                    new_url_1 = re.sub(r'(starttime=.*&endtime)=.*(&advancedfilter)', r'\1=%s\2' % day_string,
                                       response.url)
                    # print(new_url_1)
                    yield Request(new_url_1, callback=self.parse)
                    day_string = (new_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                    new_url_2 = re.sub(r'(starttime)=.*(&endtime=.*&advancedfilter)', r'\1=%s\2' % day_string,
                                       response.url)
                    yield Request(new_url_2, callback=self.parse)
                    return
                else:
                    for page_num in range(2, all_page + 1):
                        page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                        yield Request(page_url, self.parse, dont_filter=True, meta=response.meta)

        tree_node = etree.HTML(response.body)
        tweet_nodes = tree_node.xpath('//div[@class="c" and @id]')
        for tweet_node in tweet_nodes:
            try:
                tweet_item = TweetItem()
                if response.url.endswith('page=1'):
                    tweet_item['user_name'] = ''.join(
                        tree_node.xpath('.//div[@class="ut"]/span[@class="ctt"][1]/text()[1]'))
                else:
                    name_text = ''.join(tree_node.xpath('.//div[@class="ut"]/text()'))
                    user_name = ''.join(re.findall(r'(.*)的微博', name_text))
                    if user_name != '':
                        tweet_item['user_name'] = user_name
                    else:
                        tweet_item['user_name'] = name_text
                tweet_item['crawl_time'] = int(time.time())
                tweet_repost_url = tweet_node.xpath('.//a[contains(text(),"转发[")]/@href')[0]
                user_tweet_id = re.search(r'/repost/(.*?)\?uid=(\d+)', tweet_repost_url)
                tweet_item['weibo_url'] = 'https://weibo.com/{}/{}'.format(user_tweet_id.group(2),
                                                                           user_tweet_id.group(1))
                tweet_item['user_id'] = user_tweet_id.group(2)
                tweet_item['_id'] = user_tweet_id.group(1)
                create_time_info_node = tweet_node.xpath('.//span[@class="ct"]')[-1]
                create_time_info = create_time_info_node.xpath('string(.)')
                if "来自" in create_time_info:
                    tweet_item['created_at'] = time_fix(create_time_info.split('来自')[0].strip())
                    tweet_item['tool'] = create_time_info.split('来自')[1].strip()
                else:
                    tweet_item['created_at'] = time_fix(create_time_info.strip())

                like_num = tweet_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
                tweet_item['like_num'] = int(re.search(r'\d+', like_num).group())

                repost_num = tweet_node.xpath('.//a[contains(text(),"转发[")]/text()')[-1]
                tweet_item['repost_num'] = int(re.search(r'\d+', repost_num).group())

                comment_num = tweet_node.xpath(
                    './/a[contains(text(),"评论[") and not(contains(text(),"原文"))]/text()')[-1]
                tweet_item['comment_num'] = int(re.search(r'\d+', comment_num).group())

                image_count = ''.join(tweet_node.xpath('.//a[contains(text(),"组图共")]/text()'))
                if image_count:
                    tweet_item['image_count'] = re.findall(r'组图共(\d+)张', image_count)[0]
                    tweet_item['image_url'] = ''.join(tweet_node.xpath('.//a[contains(text(),"组图共")]/@href'))
                else:
                    tweet_item['image_url'] = ''.join(tweet_node.xpath('.//img[@alt="图片"]/@src'))
                    if len(tweet_item['image_url']) > 0:
                        tweet_item['image_count'] = 1

                tweet_item['repost_image_url'] = ','.join(
                    tweet_node.xpath('.//div/a[contains(text(),"查看图片")]/@href'))

                videos = tweet_node.xpath('.//a[contains(@href,"https://m.weibo.cn/s/video/show?object_id=")]/@href')
                if videos:
                    tweet_item['video_url'] = videos

                map_node = tweet_node.xpath('.//a[contains(text(),"显示地图")]')
                if map_node:
                    map_node = map_node[0]
                    map_node_url = map_node.xpath('./@href')[0]
                    map_info = re.search(r'xy=(.*?)&', map_node_url).group(1)
                    tweet_item['location_map_info'] = map_info

                repost_node = tweet_node.xpath('.//a[contains(text(),"原文评论[")]/@href')
                if repost_node:
                    tweet_item['origin_weibo'] = repost_node[0]

                all_content_link = tweet_node.xpath('.//a[text()="全文" and contains(@href,"ckAll=1")]')
                if all_content_link:
                    all_content_url = self.base_url + all_content_link[0].xpath('./@href')[0]
                    yield Request(all_content_url, callback=self.parse_all_content, meta={'item': tweet_item},
                                  priority=1)
                else:
                    tweet_html = etree.tostring(tweet_node, encoding='unicode')
                    tweet_item['content'] = extract_weibo_content(tweet_html).replace(',', '，')
                    yield tweet_item

            except Exception as e:
                self.logger.error(e)

    def parse_all_content(self, response):
        tree_node = etree.HTML(response.body)
        tweet_item = response.meta['item']
        content_node = tree_node.xpath('//*[@id="M_"]/div[1]')[0]
        tweet_html = etree.tostring(content_node, encoding='unicode')
        tweet_item['content'] = extract_weibo_content(tweet_html).replace(',', '，')
        yield tweet_item
