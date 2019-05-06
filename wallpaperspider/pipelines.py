# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class WallpaperspiderPipeline(object):
    def process_item(self, item, spider):



        return item


class WallhavenMongoDBPipline(object):

    mongo_uri = "mongodb://127.0.0.1"

    collection_name = "wallhaven"

    db_name = "wallpaper"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(WallhavenMongoDBPipline.mongo_uri)
        self.db = self.client[WallhavenMongoDBPipline.db_name]


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[WallhavenMongoDBPipline.collection_name].insert_one(dict(item))
        return item
