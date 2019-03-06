# -*- coding: utf-8 -*-
import re

import scrapy
import requests
from lxml import etree

import wallpaperspider


class WallhavenSpider(scrapy.Spider):
    name = 'wallhaven'
    allowed_domains = ['https://alpha.wallhaven.cc']
    start_urls = ['https://alpha.wallhaven.cc/']

    _cookie = None

    def start_requests(self):

        header = wallpaperspider.DEFAULT_REQUEST_HEADERS.copy()
        header["User-Agent"] = wallpaperspider.USER_AGENT
        resp = requests.get(url="https://alpha.wallhaven.cc/auth/login", headers=header)

        parser = etree.HTML(resp.text)

        _token = str(parser.xpath('//*[@id="login"]/input/@value')[0])

        resp = requests.post(url="https://alpha.wallhaven.cc/auth/login", data={"_token": _token, "username": "vaskka@outlook.com", "password": "czm19990216"}, headers=header)

        WallhavenSpider._cookies = resp.cookies.get_dict()

        # 获取全部页数

        resp = requests.get(url="https://alpha.wallhaven.cc/latest", headers=header, cookies=WallhavenSpider._cookies)
        parser = etree.HTML(resp.text)
        max_page_text = parser.xpath('//*[@id="thumbs"]/section/header/h2/text()')[1]

        max_num_result = re.match(".*?(\d+)", max_page_text)
        max_page = int(max_num_result.group(1))

        # generate
        for i in range(1, max_page + 1):
            yield scrapy.Request(url="https://alpha.wallhaven.cc/latest?page=" + str(i), callback=self.parse, cookies=WallhavenSpider._cookies)

        pass

    def parse(self, response):


        pass
