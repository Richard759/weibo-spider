#!/usr/bin/env python
# encoding: utf-8
import re
import datetime
import execjs
import math


def time_fix(time_string):
    now_time = datetime.datetime.now()
    if '分钟前' in time_string:
        minutes = re.search(r'^(\d+)分钟', time_string).group(1)
        created_at = now_time - datetime.timedelta(minutes=int(minutes))
        return created_at.strftime('%Y-%m-%d %H:%M')

    if '小时前' in time_string:
        minutes = re.search(r'^(\d+)小时', time_string).group(1)
        created_at = now_time - datetime.timedelta(hours=int(minutes))
        return created_at.strftime('%Y-%m-%d %H:%M')

    if '今天' in time_string:
        return time_string.replace('今天', now_time.strftime('%Y-%m-%d'))

    if '月' in time_string:
        time_string = time_string.replace('月', '-').replace('日', '')
        time_string = str(now_time.year) + '-' + time_string
        return time_string

    return time_string


keyword_re = re.compile('<span class="kt">|</span>|原图|<!-- 是否进行翻译 -->|<span class="cmt">|\[组图共.+张\]')
emoji_re = re.compile('<img alt="|" src="//h5\.sinaimg(.*?)/>')
white_space_re = re.compile('<br />')
div_re = re.compile('</div>|<div>')
image_re = re.compile('<img(.*?)/>')
url_re = re.compile('<a href=(.*?)>|</a>')


def extract_weibo_content(weibo_html):
    s = weibo_html
    if 'class="ctt">' in s:
        s = s.split('class="ctt">', maxsplit=1)[1]
    s = emoji_re.sub('', s)
    s = url_re.sub('', s)
    s = div_re.sub('', s)
    s = image_re.sub('', s)
    if '<span class="ct">' in s:
        s = s.split('<span class="ct">')[0]
    splits = s.split('赞[')
    if len(splits) == 2:
        s = splits[0]
    if len(splits) == 3:
        origin_text = splits[0]
        retweet_text = splits[1].split('转发理由:')[1]
        s = origin_text + '转发理由:' + retweet_text
    s = white_space_re.sub(' ', s)
    s = keyword_re.sub('', s)
    s = s.replace('\xa0', '')
    s = s.strip(':')
    s = s.strip()
    return s


def extract_comment_content(comment_html):
    s = comment_html
    if 'class="ctt">' in s:
        s = s.split('class="ctt">', maxsplit=1)[1]
    s = s.split('举报', maxsplit=1)[0]
    s = emoji_re.sub('', s)
    s = keyword_re.sub('', s)
    s = url_re.sub('', s)
    s = div_re.sub('', s)
    s = image_re.sub('', s)
    s = white_space_re.sub(' ', s)
    s = s.replace('\xa0', '')
    s = s.strip(':')
    s = s.strip()
    return s


def extract_repost_content(repost_html):
    s = repost_html
    if 'class="cc">' in s:
        s = s.split('<span class="cc">', maxsplit=1)[0]
    s = emoji_re.sub('', s)
    s = keyword_re.sub('', s)
    s = url_re.sub('', s)
    s = div_re.sub('', s)
    s = image_re.sub('', s)
    s = white_space_re.sub(' ', s)
    s = s.replace('\xa0', '')
    s = s.replace('<div class="c">', '')
    s = s.strip(':')
    s = s.strip()
    return s


str62keys = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def str62to10(str62):
    i10 = 0
    for i in range(len(str62)):
        n = len(str62) - i - 1
        s = str62[i]
        i10 += str62keys.index(s) * math.pow(62, n)
    return int(i10)


def int10to62(int10):
    s62 = ''
    while int10 != 0:
        r = int10 % 62
        s62 = str62keys[r] + s62
        int10 = math.floor(int10 / 62)
    return s62


def mid2id(mid):
    cid = ''
    for i in range(len(mid) - 4, -4, -4):
        if i < 0:
            offset1 = 0
        else:
            offset1 = i
        if i < 0:
            mid_len = len(mid) % 4
        else:
            mid_len = 4
        mid_str = mid[offset1:offset1 + mid_len]
        mid_str = str(str62to10(mid_str))
        if offset1 > 0:
            while len(mid_str) < 7:
                mid_str = '0' + mid_str
        cid = mid_str + cid
    return cid


def id2mid(_id):
    mid = ''
    for i in range(len(_id) - 7, -7, - 7):
        if i < 0:
            offset1 = 0
        else:
            offset1 = i
        offset2 = i + 7
        num = _id[offset1:offset2]
        num = int10to62(int(num))
        mid = num + mid
    return mid


def get_create_time(str_time):
    if re.match(r'^20..年..月..日.*', str_time):
        time_index = f'{str_time[0:4]}-{str_time[5:7]}-{str_time[8:10]} {str_time[11:]}'
    elif re.match(r'^..月..日.*', str_time):
        time_index = f'{datetime.date.today().year}-{str_time[0:2]}-{str_time[3:5]} {str_time[6:]}'
    elif re.match(r'^今天.*', str_time):
        time_index = f'{datetime.date.today()} {str_time[2:]}'
    elif len(re.findall(r'(.*)-(.*)-(.*) (.*)', str_time)) > 0:
        (year, month, day, mh) = re.findall(r'(.*)-(.*)-(.*) (.*)', str_time)[0]
        time_index = '%s-%02d-%02d %s' % (year, int(month), int(day), mh)
    else:
        time_index = str_time
    return time_index
