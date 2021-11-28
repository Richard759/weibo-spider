# -*- coding: utf-8 -*-

BOT_NAME = 'spider'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ROBOTSTXT_OBEY = False
HTTPERROR_ALLOWED_CODES = [403]
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

TWEET_ID = []
with open('tweet_ids.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        TWEET_ID.append(line.strip())

COOKIES_ENABLED = False

# change cookie to yours
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29',
    'Cookie': 'SINAGLOBAL=2984020340573.4653.1615966504509; UOR=,,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh5h_i4eSgoD7jFisEd1k8Y5JpX5KMhUgL.FoqfSo.feKzfSK52dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcSKq4SK2ESK-7; wvr=6; ALF=1669472766; SSOLoginState=1637936767; SCF=At9eOLw9o69sap1_tTXMdkUPPcB7_jux_87EDPewfgITWtyxf3dfk6upyGZAhRpVaaFNryrPm9vHBCQXMkxqxO0.; SUB=_2A25MpJ4vDeRhGeBL7VsU8SzJzjyIHXVv04jnrDV8PUNbmtAKLW_AkW9NRvFrV5idC9PRnC3NasseKr-pbS_1DMuf; _s_tentry=-; Apache=786128725966.9614.1637936769970; ULV=1637936769994:45:10:5:786128725966.9614.1637936769970:1637914387575; webim_unReadCount=%7B%22time%22%3A1637936772610%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A42%2C%22msgbox%22%3A0%7D; WBStorage=5fd44921|undefined'}
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
