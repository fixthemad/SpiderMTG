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
        self.ws.cell(row=1, column=1, value='Card')
        self.ws.cell(row=1, column=2, value='Title')
        self.ws.cell(row=1, column=3, value='Price')
        self.ws.cell(row=1, column=4, value='Quantity')
        self.ws.cell(row=1, column=5, value='Expansion')
        self.ws.cell(row=1, column=6, value='Language')
        self.ws.cell(row=1, column=7, value='Extra')
        self.ws.cell(row=1, column=8, value='Link')
        self.ws.cell(row=1, column=9, value='Bids')
        self.ws.cell(row=1, column=10, value='Time Left')

    def close_spider(self, spider):
        self.wb.save('auctions.xlsx')

    def write_to_workbook(self, item):
        pass

    def process_item(self, item, spider):
        row = self.ws[self.ws.max_row + 1]

        card = item['card']
        if len(card) > 1:
            card_str = "{pt}/{eng}".format(pt=card[0],eng=card[1])
        else:
            card_str = card[0]
        row[0].value = card_str
        row[1].value = str(item['title'])
        row[2].value = str(item['price'])
        row[3].value = str(item['quantity'])

        exp = item['expansion']
        if len(exp) > 1:
            exp_str = "{pt}/{eng}".format(pt=exp[0],eng=exp[1])
        else:
            exp_str = exp[0]
        row[4].value = exp_str

        row[5].value = str(item['language'])
        try:
            row[6].value = str(item['extra'])
        except KeyError as e:
            pass
        row[7].value = str(item['href'])
        row[8].value = str(item['bids'])
        row[9].value = str(item['time_left'])

        return item
