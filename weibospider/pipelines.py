# -*- coding: utf-8 -*-
import csv


class CsvFilePipeline(object):
    def __init__(self):
        f_u = open("Users.csv", 'w', encoding='utf-8-sig', newline='')
        f_t = open("Tweets.csv", 'w', encoding='utf-8-sig', newline='')
        f_c = open("Comments.csv", 'w', encoding='utf-8-sig', newline='')
        f_r = open("Relationships.csv", 'w', encoding='utf-8-sig', newline='')
        f_rp = open("Reposts.csv", 'w', encoding='utf-8-sig', newline='')
        fieldnames_u = ['_id', 'nick_name', 'gender', 'province', 'city', 'brief_introduction',
                        'birthday', 'tweets_num', 'follows_num', 'fans_num', 'sex_orientation',
                        'sentiment', 'vip_level', 'authentication', 'person_url', 'labels', 'crawl_time']
        fieldnames_t = ["_id", "comment_num", "content", "crawl_time", "created_at", "image_url", "like_num",
                        "location_map_info", "origin_weibo", "repost_num", "tool", "user_id", "weibo_url"]
        fieldnames_c = ['_id', 'comment_user_id', 'content', 'weibo_id', 'created_at', 'like_num', 'crawl_time']
        fieldnames_r = ['_id', 'fan_id', 'followed_id', 'crawl_time']
        fieldnames_rp = ['_id', 'user_id', 'content', 'weibo_id', 'created_at', 'crawl_time']
        self.Users = csv.DictWriter(f_u, fieldnames=fieldnames_u)
        self.Tweets = csv.DictWriter(f_t, fieldnames=fieldnames_t)
        self.Comments = csv.DictWriter(f_c, fieldnames=fieldnames_c)
        self.Relationships = csv.DictWriter(f_r, fieldnames=fieldnames_r)
        self.Reposts = csv.DictWriter(f_rp, fieldnames=fieldnames_rp)
        self.Tweets.writeheader()
        self.Comments.writeheader()
        self.Relationships.writeheader()
        self.Reposts.writeheader()
        self.Users.writeheader()

    def process_item(self, item, spider):
        if spider.name == 'comment_spider':
            self.insert_item(self.Comments, item)
        elif spider.name == 'fan_spider':
            self.insert_item(self.Relationships, item)
        elif spider.name == 'follower_spider':
            self.insert_item(self.Relationships, item)
        elif spider.name == 'user_spider':
            self.insert_item(self.Users, item)
        elif spider.name == 'tweet_spider':
            self.insert_item(self.Tweets, item)
        elif spider.name == 'repost_spider':
            self.insert_item(self.Reposts, item)
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.writerow(dict(item))
        except Exception as e:
            print(e)
            pass
