# -*- coding: utf-8 -*-

BOT_NAME = 'spider'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ROBOTSTXT_OBEY = False
HTTPERROR_ALLOWED_CODES = [403]

# change cookie to yours
NEW_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29',
    'Cookie': 'SINAGLOBAL=2148060604709.9827.1634031842495; ALF=1666368143; SCF=AprdIWy1ZOmUIhaGeBwe-KtkManKmfz1fqRMy9MDxGidQ4F0PgXSAw9hr6r86YTVWrWSf3scgv5yjDOEbYOqtnE.; UOR=,,login.sina.com.cn; SUB=_2A25Mdm75DeRhGeBL7VsU8SzJzjyIHXVvmXKxrDV8PUJbkNB-LW-kkW1NRvFrV2G_6rmQsCtNbFFUyZ-Tb8g__SCU; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh5h_i4eSgoD7jFisEd1k8Y5NHD95QcSKq4SK2ESK-7Ws4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSo-c1K-peo-fe5tt; _ga=GA1.2.1364046298.1636980536; __gads=ID=66f0d7986700199d:T=1636980536:S=ALNI_MaPK7Ff2l1ASqs0HUB3GamPgZoQqA; _s_tentry=-; Apache=4633044387551.415.1638185651594; ULV=1638185651598:5:3:1:4633044387551.415.1638185651594:1637201767844; WBStorage=5fd44921|undefined'}

# OLD_HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29',
#     'Cookie': 'SCF=AprdIWy1ZOmUIhaGeBwe-KtkManKmfz1fqRMy9MDxGidVL9IrqGMLuV9Cldh9AXCWYrL7C7n7sz5m0im7uMwZlI.; SUB=_2A25Mdm75DeRhGeBL7VsU8SzJzjyIHXVvmXKxrDV6PUJbktB-LXfkkW1NRvFrVwW90yQ3_mKawwMojDKt2fcqo_XG; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh5h_i4eSgoD7jFisEd1k8Y5NHD95QcSKq4SK2ESK-7Ws4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSo-c1K-peo-fe5tt; _T_WM=82f38f3e7008c06bb3e515382d023607'}

# 选择用weibo.cn/s.weibo.com的cookie
DEFAULT_REQUEST_HEADERS = NEW_HEADERS

# 原创微博和热门微博同时只能满足一个
ONLY_HOT = True
ONLY_ORIGIN = False

# 爬虫时间间隔
TIME_DELTA = 1

TWEET_DATE_WINDOW = {
    'start_date': '2020-06-01',
    'end_date': '2021-11-20'
}

fff = ['中华文化', '创意文化', '文化']
lll = ['奇妙游', '河南卫视']
TWEET_KEY_WORDS = []

for ff in fff:
    for ll in lll:
        TWEET_KEY_WORDS.append(ff + ll)

# TWEET_KEY_WORDS = [
#     "丽江抢劫",
#     "丽江毁容",
#     "丽江打人"
# ]

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
