# -*- coding: utf-8 -*-
import time
import scrapy
from scrapy_proxy_crawler.items import *

class ProxySpiderSpider(scrapy.Spider):
    name = 'proxy_spider'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        #'User-Agent' : 'Baiduspider',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded;utf-8',
        'X-Requested-With': 'XMLHttpRequest',
    }

    def __init__(self, proxy_check_url, max_need_proxy=100):
        self.proxy_check_url = proxy_check_url
        self.max_need_proxy = int(max_need_proxy)
        self.accepted_proxy_num = 0

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        settings = crawler.settings
        proxy_check_url = settings.get('PROXY_CHECK_URL', None)
        proxy_check_url = kwargs.get('proxy_check_url', proxy_check_url)
        if 'proxy_check_url' in kwargs:
            del kwargs['proxy_check_url']
        max_need_proxy = settings.get('MAX_NEED_PROXY', 100)
        max_need_proxy = kwargs.get('max_need_proxy', max_need_proxy)
        if 'max_need_proxy' in kwargs:
            del kwargs['max_need_proxy']
        return cls(proxy_check_url, max_need_proxy=max_need_proxy, *args, **kwargs)

    def start_requests(self):
        self.logger.info('Start with max need proxy %d' % self.max_need_proxy)
        for item in self.start_kuaidaili():
            yield item
        for item in self.start_66ip():
            yield item
        for item in self.start_xicidaili():
            yield item


    def start_kuaidaili(self):
        i = 1
        url = 'http://www.kuaidaili.com/free/inha/%d/'%i
        yield scrapy.Request(url=url,
                             headers=self.headers,
                             callback=self.parse_kuaidaili,
                             meta={'idx': i})

    def start_66ip(self):
        urls = [
            'http://www.66ip.cn/mo.php?sxb=%B1%B1%BE%A9&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=',
            'http://www.66ip.cn/mo.php?sxb=%C9%CF%BA%A3&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=',
            'http://www.66ip.cn/mo.php?sxb=%B9%E3%B6%AB&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=',
            'http://www.66ip.cn/mo.php?sxb=%BD%AD%CB%D5&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=',
            'http://www.66ip.cn/mo.php?sxb=%D5%E3%BD%AD&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=',
            'http://www.66ip.cn/mo.php?sxb=%CB%C4%B4%A8&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=',
        ]
        for url in urls:
            time.sleep(5)
            yield scrapy.Request(url=url,
                                 headers=self.headers,
                                 callback=self.parse_66ip)

    def start_xicidaili(self):
        i = 1
        url = 'http://www.xicidaili.com/wt/%d' % i
        yield scrapy.Request(url=url,
                             headers=self.headers,
                             callback=self.parse_xicidaili,
                             meta={'idx': i})

    def parse_66ip(self, response):
        selector = scrapy.selector.Selector(response)
        proxys = selector.re('(\d+\.\d+\.\d+\.\d+:\d+)')
        proxys = ["http://" + item for item in proxys]
        for item in self.check_proxy(proxys):
            yield item

    def parse_kuaidaili(self, response):

        ips = response.css('#list > table > tbody > tr > td:nth-child(1)::text').extract()
        ports = response.css('#list > table > tbody > tr > td:nth-child(2)::text').extract()
        proxys = ['http://%s:%s' % (ip, port) for ip, port in zip(ips, ports)]
        for item in self.check_proxy(proxys):
            yield item
        time.sleep(5)
        i = response.meta['idx'] + 1
        if i <= 10:
            url = 'http://www.kuaidaili.com/free/inha/%d/' % i
            yield scrapy.Request(url=url,
                                 headers=self.headers,
                                 callback=self.parse_kuaidaili,
                                 meta={'idx': i})

    def parse_xicidaili(self, response):
        ips = response.css('#ip_list >  tr > td:nth-child(2)::text').extract()
        ports = response.css('#ip_list > tr > td:nth-child(3)::text').extract()
        proxys = ['http://%s:%s' % (ip, port) for ip, port in zip(ips, ports)]
        for item in self.check_proxy(proxys):
            yield item
        time.sleep(5)
        i = response.meta['idx'] + 1
        if i <= 10:
            url = 'http://www.xicidaili.com/wt/%d' % i
            yield scrapy.Request(url=url,
                                 headers=self.headers,
                                 callback=self.parse_xicidaili,
                                 meta={'idx': i})

    def check_proxy(self, proxys):
        for proxy in proxys:
            url = self.proxy_check_url
            yield scrapy.Request(url=url,
                                 dont_filter=True,
                                 headers=self.headers,
                                 callback=self.parse_check_proxy,
                                 meta={'proxy': proxy,
                                       'dont_retry': True})

    def parse_check_proxy(self, response):
        item = ProxyItem()
        item['addr'] = response.meta['proxy']
        yield item
        self.accepted_proxy_num = self.accepted_proxy_num + 1
        if self.accepted_proxy_num >= self.max_need_proxy:
            raise scrapy.exceptions.CloseSpider('finished to got %d proxy.' % self.accepted_proxy_num)
