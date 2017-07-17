# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from openpyxl import Workbook
from SpiderMTG.items import Auction


class ExcelWriter(object):

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active

    def open_spider(self, spider):
        print("Opened")

    def close_spider(self, spider):
        self.wb.save('test.xlsx')

    def write_to_workbook(self, item):
        pass

    def process_item(self, item, spider):
        print("!" + item)
        return item
