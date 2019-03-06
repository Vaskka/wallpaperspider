# -*- coding: utf-8 -*-
import scrapy


class WallhavenSpider(scrapy.Spider):
    name = 'wallhaven'
    allowed_domains = ['https://alpha.wallhaven.cc']
    start_urls = ['http://https://alpha.wallhaven.cc/']

    def parse(self, response):
        pass
