# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy_proxy_crawler.items import *

class ScrapyProxyCrawlerPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, ProxyItem):
            spider.logger.info("Accepted proxy: %s" % item['addr'])
        return item