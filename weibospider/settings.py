# -*- coding: utf-8 -*-

BOT_NAME = 'spider'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ROBOTSTXT_OBEY = False
HTTPERROR_ALLOWED_CODES = [403]

# change cookie to yours

# 选择用weibo.cn/s.weibo.com的cookie
DEFAULT_REQUEST_HEADERS = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Dest": "script",
    'Accept': '*/*',
    'Cookie': 'SINAGLOBAL=2984020340573.4653.1615966504509; UOR=,,weibo.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh5h_i4eSgoD7jFisEd1k8Y5JpX5KMhUgL.FoqfSo.feKzfSK52dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcSKq4SK2ESK-7; ALF=1674035183; SSOLoginState=1642499183; SCF=At9eOLw9o69sap1_tTXMdkUPPcB7_jux_87EDPewfgITtHbaiNZK1nrM8XtmUUXdL51qYLg9Up26LdgzfmgMQK4.; SUB=_2A25M4vwjDeRhGeBL7VsU8SzJzjyIHXVvlmrrrDV8PUNbmtAKLXKskW9NRvFrVx222uUyzlM8P_ckVZdFkeX_apMP; wvr=6; _s_tentry=-; Apache=2946296110125.0063.1642499203297; ULV=1642499203315:63:4:1:2946296110125.0063.1642499203297:1641968717546; wb_view_log_6569512550=1920*10801^%^261920*10801.100000023841858; webim_unReadCount=^%^7B^%^22time^%^22^%^3A1642515047668^%^2C^%^22dm_pub_total^%^22^%^3A0^%^2C^%^22chat_group_client^%^22^%^3A0^%^2C^%^22chat_group_notice^%^22^%^3A0^%^2C^%^22allcountNum^%^22^%^3A36^%^2C^%^22msgbox^%^22^%^3A0^%^7D'
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

CHILD_COMMENT_URL = []

with open('comment_urls.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        url = line.strip()
        if len(url) != 0:
            CHILD_COMMENT_URL.append(url)

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
