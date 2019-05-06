# -*- coding: utf-8 -*-
import json
import os
import re

import scrapy
import requests
from lxml import etree
from scrapy.loader import ItemLoader
from ..settings import *
from .utils import util

import wallpaperspider
from wallpaperspider.items import WallPaperImageItem


class WallhavenSpider(scrapy.Spider):
    name = 'wallhaven'
    allowed_domains = ['alpha.wallhaven.cc']
    start_urls = ['https://alpha.wallhaven.cc/latest']

    _cookies = None

    def start_requests(self):
        header = {
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'zh-CN,zh;q=0.9',
          'Connection': 'Keep-Alive'
        }
        # cookie_file = str(BASE_DIR + os.path.sep + "cookie.json")
        #
        # if os.path.exists(cookie_file):
        #     with open(cookie_file, "r") as f:
        #         WallhavenSpider._cookies = json.loads(f.read())
        # else:
        #
        #     header["User-Agent"] = wallpaperspider.USER_AGENT
        #     resp = requests.get(url="https://alpha.wallhaven.cc/auth/login", headers=header)
        #
        #     parser = etree.HTML(resp.text)
        #
        #     _token = str(parser.xpath("//*[@id='login']/input[@name='_token']/@value")[0])
        #
        #     print(_token)
        #
        #     resp = requests.post(url="https://alpha.wallhaven.cc/auth/login", data={"_token": _token, "username": "vaskka@outlook.com", "password": "czm19990216"}, headers=header)
        #
        #     WallhavenSpider._cookies = resp.cookies.get_dict()
        #
        #     with open(cookie_file, "w") as f:
        #         f.write(json.dumps(WallhavenSpider._cookies))

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

        all_url = response.xpath("//a/@href").getall()
        for u in all_url.copy():
            re_result = re.match("^https://alpha\.wallhaven\.cc/wallpaper/[0-9]+$", u)
            if re_result:
                yield scrapy.Request(url=u, callback=self.parse_item,
                                     cookies=self._cookies)

        pass

    def parse_item(self, response):



        loader = ItemLoader(item=WallPaperImageItem(), response=response)

        # 图片url
        iu = "https:" + response.xpath('//*[@id="wallpaper"]/@src')[0].root
        loader.add_value('image_url', iu)

        loader.add_xpath('tags', '//*[@id="tags"]/li/a/text()')

        loader.add_xpath('category', '//*[@id="showcase-sidebar"]/div/div[1]/div[2]/dl/dd[2]/text()')

        loader.add_xpath('size', "//*[@id='showcase-sidebar']/div/div[1]/h3/text()")

        loader.add_xpath('colors', '//*[@id="showcase-sidebar"]/div/div[1]/ul/li/a/@href')

        loader.add_xpath('original', '//a[contains(@class,"username")]/@href')

        loader.add_value('original_id', util.from_url_get_id(str(response._url)))

        return loader.load_item()
        pass
