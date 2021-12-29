# -*- coding: utf-8 -*-

BOT_NAME = 'spider'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ROBOTSTXT_OBEY = False
HTTPERROR_ALLOWED_CODES = [403]

# change cookie to yours

# 选择用weibo.cn/s.weibo.com的cookie
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29',
    'Cookie': '_T_WM=ef7ab575ffcc39e2dd7867b01b0f06ef; SCF=AprdIWy1ZOmUIhaGeBwe-KtkManKmfz1fqRMy9MDxGid-osKJWn1_KBi5kESQALwavt1nB2EeWqBT0U_KVRHnQA.; SUB=_2A25MyCbnDeRhGeBL7VsU8SzJzjyIHXVsM0qvrDV6PUJbktAKLU2ikW1NRvFrV3Qjn8ro-qvKbyNyPp9tGiTNWNly; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh5h_i4eSgoD7jFisEd1k8Y5NHD95QcSKq4SK2ESK-7Ws4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSo-c1K-peo-fe5tt; SSOLoginState=1640781495'
}


# 原创微博和热门微博同时只能满足一个
ONLY_HOT = False
ONLY_ORIGIN = False

# 爬虫时间间隔
MAX_DELTA = 10

TWEET_DATE_WINDOW = {
    'start_date': '2017-01-01',
    'end_date': '2017-03-01'
}

# fff = ['中华文化', '创意文化', '文化']
# lll = ['奇妙游', '河南卫视']
# TWEET_KEY_WORDS = []
#
# for ff in fff:
#     for ll in lll:
#         TWEET_KEY_WORDS.append(ff + ll)

TWEET_KEY_WORDS = [
    '丽江打人',
    '丽江毁容',
    '丽江抢劫'
]

COMMENT_TWEET_ID = []

with open('comment_tweet_ids.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        COMMENT_TWEET_ID.append(line.strip())

REPOST_TWEET_ID = []

with open('repost_tweet_ids.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        REPOST_TWEET_ID.append(line.strip())


USER_ID = []

with open('user_ids.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        USER_ID.append(line.strip())

USER_TWEET_ID = []
with open('user_tweet_ids.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        USER_TWEET_ID.append(line.strip())
# 不用修改的设置

COOKIES_ENABLED = False

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'middlewares.IPProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 101,
}

ITEM_PIPELINES = {
    'pipelines.CsvFilePipeline': 300,
}
