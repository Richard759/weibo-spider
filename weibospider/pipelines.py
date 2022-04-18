# -*- coding: utf-8 -*-
import csv
from run_spider import mode


class CsvFilePipeline(object):
    def __init__(self):
        if mode == 'user':
            f_u = open("Users.csv", 'w', encoding='utf-8-sig', newline='')
            fieldnames_u = ['_id', 'nick_name', 'gender', 'province', 'city', 'brief_introduction',
                            'birthday', 'tweets_num', 'follows_num', 'fans_num', 'sex_orientation',
                            'sentiment', 'vip_level', 'authentication', 'labels', 'crawl_time']
            self.Users = csv.DictWriter(f_u, fieldnames=fieldnames_u)
            self.Users.writeheader()
        elif mode == 'user_brief':
            f_u = open("UsersBrief.csv", 'w', encoding='utf-8-sig', newline='')
            fieldnames_u = ['_id', 'tweets_num', 'follows_num', 'fans_num', 'crawl_time']
            self.UserBrief = csv.DictWriter(f_u, fieldnames=fieldnames_u)
            self.UserBrief.writeheader()
        elif mode == 'fan':
            f_r = open("fans.csv", 'w', encoding='utf-8-sig', newline='')
            fieldnames_r = ['_id', 'fan_id', 'followed_id', 'crawl_time']
            self.Relationships = csv.DictWriter(f_r, fieldnames=fieldnames_r)
            self.Relationships.writeheader()
        elif mode == 'follow':
            f_r = open("followers.csv", 'w', encoding='utf-8-sig', newline='')
            fieldnames_r = ['_id', 'fan_id', 'followed_id', 'crawl_time']
            self.Relationships = csv.DictWriter(f_r, fieldnames=fieldnames_r)
            self.Relationships.writeheader()
        elif mode == 'tweet' or mode == 'user_tweet':
            f_t = open("Tweets.csv", 'w', encoding='utf-8-sig', newline='')
            fieldnames_t = ["_id", "crawl_time", "content", "created_at", "user_id", "user_name", "image_count",
                            "image_url", "repost_image_url", "like_num", "comment_num", "repost_num", "video_url",
                            "location_map_info", "origin_weibo", "tool", "weibo_url"]
            self.Tweets = csv.DictWriter(f_t, fieldnames=fieldnames_t)
            self.Tweets.writeheader()
        elif mode == 'comment':
            f_c = open("Comments.csv", 'w', encoding='utf-8-sig', newline='')
            fieldnames_c = ['_id', 'comment_user_id', 'comment_user', 'content', 'weibo_id',
                            'created_at', 'like_num', 'crawl_time', 'child_url']
            self.Comments = csv.DictWriter(f_c, fieldnames=fieldnames_c)
            self.Comments.writeheader()
        elif mode == 'child_comment':
            f_c = open("child_comment.csv", 'w', encoding='utf-8-sig', newline='')
            fieldnames_c = ['_id', 'comment_user_id', 'comment_user', 'root_comment_id', 'content', 'weibo_id',
                            'created_at', 'like_num', 'crawl_time']
            self.ChildComment = csv.DictWriter(f_c, fieldnames=fieldnames_c)
            self.ChildComment.writeheader()
        elif mode == 'repost':
            f_rp = open("Reposts.csv", 'w', encoding='utf-8-sig', newline='')
            fieldnames_rp = ['_id', 'user_id', 'content', 'weibo_id', 'created_at', 'crawl_time']
            self.Reposts = csv.DictWriter(f_rp, fieldnames=fieldnames_rp)
            self.Reposts.writeheader()

    def process_item(self, item, spider):
        if spider.name == 'comment_spider':
            self.insert_item(self.Comments, item)
        elif spider.name == 'child_comment_spider':
            self.insert_item(self.ChildComment, item)
        elif spider.name == 'fan_spider':
            self.insert_item(self.Relationships, item)
        elif spider.name == 'follower_spider':
            self.insert_item(self.Relationships, item)
        elif spider.name == 'user_spider':
            self.insert_item(self.Users, item)
        elif spider.name == 'user_brief_spider':
            self.insert_item(self.UserBrief, item)
        elif spider.name == 'tweet_spider' or spider.name == 'user_tweet_spider':
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
