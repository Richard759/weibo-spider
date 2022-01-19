#!/usr/bin/env python
# encoding: utf-8
import re
import datetime
import execjs


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


jspython = '''str62keys = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
/**
* 10进制值转换为62进制
* @param {String} int10 10进制值
* @return {String} 62进制值
*/
function int10to62(int10) {
    var s62 = '';
    var r = 0;
    while (int10 != 0) {
            r = int10 % 62;
            s62 = this.str62keys.charAt(r) + s62;
            int10 = Math.floor(int10 / 62);
    }
    return s62;
}
/**
* 62进制值转换为10进制
* @param {String} str62 62进制值
* @return {String} 10进制值
*/
function str62to10(str62) {
    var i10 = 0;
    for (var i = 0; i < str62.length; i++) {
            var n = str62.length - i - 1;
            var s = str62.substr(i, 1);  // str62[i]; 字符串用数组方式获取，IE下不支持为“undefined”
            i10 += parseInt(str62keys.indexOf(s)) * Math.pow(62, n);
    }
    return i10;
}
/**
* id转换为mid
* @param {String} id 微博id，如 "201110410216293360"
* @return {String} 微博mid，如 "wr4mOFqpbO"
*/
function id2mid(id) {
    if (typeof (id) != 'string') {
            return false; // id数值较大，必须为字符串！
    }
    var mid = '';
    for (var i = id.length - 7; i > -7; i = i - 7) //从最后往前以7字节为一组读取mid
    {
            var offset1 = i < 0 ? 0 : i;
            var offset2 = i + 7;
            var num = id.substring(offset1, offset2);
            num = int10to62(num);
            mid = num + mid;
    }
    return mid;
}
/**
* mid转换为id
* @param {String} mid 微博mid，如 "wr4mOFqpbO"
* @return {String} 微博id，如 "201110410216293360"
*/
function mid2id(mid) {
    var id = '';
    for (var i = mid.length - 4; i > -4; i = i - 4) //从最后往前以4字节为一组读取mid字符
    {
            var offset1 = i < 0 ? 0 : i;
            var len = i < 0 ? parseInt(mid.length % 4) : 4;
            var str = mid.substr(offset1, len);
            str = str62to10(str).toString();
            if (offset1 > 0) //若不是第一组，则不足7位补0
            {
                    while (str.length < 7) {
                            str = '0' + str;
                    }
            }
            id = str + id;
    }
    return id;
}'''

ctx = execjs.compile(jspython)  # 编译 js


def mid2id(mid):
    return ctx.call('mid2id', mid)


def id2mid(_id):
    return ctx.call('id2mid', _id)
