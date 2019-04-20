# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re

import scrapy


class WallpaperspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def from_url_get_color_str(url):
    """
    从url中提取color 16进制str
    :param url:
    :return:
    """
    r = re.match("https://alpha\.wallhaven\.cc/search\?colors=(.+)]", str(url))
    if r:
        return str(r.group(1))
    else:
        return "ffffff"
    pass


class WallPaperImageItem(WallpaperspiderItem):

    # 图片url str like https://...
    image_url = scrapy.Field()

    # tags list
    tags = scrapy.Field()

    # 分类 str
    category = scrapy.Field()

    # 图片尺寸 1234 x 5678
    size = scrapy.Field()

    # 主色调 list.len = 5
    colors = scrapy.Field(
        input_processor=from_url_get_color_str
    )

    # 原作者
    original = scrapy.Field()

    # 源网站id 234567
    original_id = scrapy.Field()

    pass


# def replace_tag_no_use_char(tag_list):
#     """
#     移除tag中空格，da
#     :param tag_list:
#     :return:
#     """
