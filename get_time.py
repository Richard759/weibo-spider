import requests
from lxml import etree
import re
import datetime

url = 'https://s.weibo.com/weibo?q=%E6%97%85%E6%B8%B8%E5%A4%A7%E6%95%B0%E6%8D%AE%E6%9D%80%E7%86%9F&typeall=1&suball=1&timescope=custom:2021-10-14:2021-10-14&Refer=g'
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68',
    'Cookie': 'SINAGLOBAL=2984020340573.4653.1615966504509; UOR=,,login.sina.com.cn; webim_unReadCount=%7B%22time%22%3A1634140865754%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D; WBStorage=6ff1c79b|undefined; ALF=1665737206; SSOLoginState=1634201206; SCF=At9eOLw9o69sap1_tTXMdkUPPcB7_jux_87EDPewfgITbo_XkYIZxnqtAdCORPhayJHTvS4wdBJN4FvhrJ6c8zc.; SUB=_2A25MY54mDeRhGeBL7VsU8SzJzjyIHXVvGIjurDV8PUNbmtB-LUGmkW9NRvFrV1eJhGmcwgERfIJ8uabY2KfVcNEu; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh5h_i4eSgoD7jFisEd1k8Y5JpX5KzhUgL.FoqfSo.feKzfSK52dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcSKq4SK2ESK-7; _s_tentry=login.sina.com.cn; Apache=4159764334623.675.1634201207591; ULV=1634201207623:31:4:3:4159764334623.675.1634201207591:1634200234499'}
res = requests.get(url, headers=headers2)
tree_node = etree.HTML(res.text)
tweet_nodes = tree_node.xpath('//div[@class="card-wrap" and @action-type="feed_list_item"]')
for tweet_node in tweet_nodes:
    info = tweet_node.xpath('.//p[@class="from"]//a[1]//text()')[-1].replace('\n', "").replace(
        '\r', "").replace(' ', "")
    if re.match(r'^20..年..月..日.*', info):
        print(123)
        time_index = f'{info[0:4]}-{info[5:7]}-{info[8:10]} {info[11:]}'
    elif re.match(r'^..月..日.*', info):
        time_index = f'2021-{info[0:2]}-{info[3:5]} {info[6:]}'
        print(123)
    elif re.match(r'^今天.*', info):
        time_index = f'{datetime.date.today()} {info[2:]}'
    else:
        time_index = info
    print(time_index)
