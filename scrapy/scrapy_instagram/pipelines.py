# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy import Spider
from items import Post

'''
class LocationFilterPipeline:
    """BODYサイズでフィルターするパイプライン"""
    def process_item(self, item: Post, spider: Spider) -> Post:
        if len(item.) < :
            raise DropItem(f'Body length less than 11000. body_length: {len(item.body)}')
        return item
'''


class ScrapyInstagramPipeline(object):
    def process_item(self, item, spider):
        return item
