import scrapy
from SpiderMTG.items import Card

def read_list_from_file(file_name):
    cards = []
    list_file = open(file_name, 'r')

    for line in list_file:
        stripped_line = line.strip()
        if stripped_line is not '':
            if stripped_line[0].isdigit():
                trimmed_line = stripped_line[2:].strip()
                if '#' in trimmed_line:
                    trimmed_line = trimmed_line[0:trimmed_line.index('#') - 1]

                cards.append(trimmed_line)

    list_file.close()

    return cards


class PricerSpider(scrapy.Spider):
    name = "pricer"
    base_url = 'http://www.mtgbrasil.com.br/index.php?route=product/search&search='
    start_urls = [
        'http://www.mtgbrasil.com.br/',
    ]

    def search_card(self, response):
        card_list = []

        products = response.xpath('//div[@class="frame-search"]'
                                  '/div[@class="product-list"]')

        names = products.xpath('.//div[@class="name"]/a/text()')
        prices = products.xpath('.//div[@class="price"]/text()')

        for name, price in zip(names, prices):
            card = Card()
            names = name.extract().strip().split("/")

            # @TODO: check if name matches the card being searched

            split_price = price.extract().strip().split("\n")
            price = split_price[0]
            quantity = split_price[1].split('(')[1].strip(')')

            card['price'] = price
            card['quantity'] = quantity


    def parse(self, response):
        if self.list_from:
            cards = read_list_from_file("Zurgo.txt")

            for card in cards:
                yield scrapy.Request(
                    url=self.base_url + card,
                    callback=self.search_card,
                )


        else:
            print("Error, no list to read from")





