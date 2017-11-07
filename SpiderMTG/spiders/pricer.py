import scrapy
from SpiderMTG.items import Card
import logging

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
            else:
                if stripped_line[0] is not '#':
                    cards.append(stripped_line)

    list_file.close()

    return cards


class PricerSpider(scrapy.Spider):
    name = "pricer"
    base_url = 'https://www.mtgbrasil.com.br/index.php?route=product/search&search='
    start_urls = [
        'https://www.mtgbrasil.com.br/',
    ]

    sites = [
        'mtgbr',
        'ug',
        'lets'
    ]

    def __init__(self, *a, **kw):
        super(PricerSpider, self).__init__(*a, **kw)
        self.search = {
            'mtgbr': self.search_card_mtgbr
        }
        self.n_cards = 0
        self.total_cards = 0

    def search_url(self, card):
        return self.base_url + card.lower()

    def search_card_mtgbr(self, response):
        card_list = []

        products = response.xpath('//div[@class="frame-search"]'
                                  '/div[@class="product-list"]')

        names = products.xpath('.//div[@class="name"]/a/text()')
        prices = products.xpath('.//div[@class="price"]/text()')

        for name, price in zip(names, prices):
            card = Card()
            trimmed_name = name.extract().strip()

            if '/' in trimmed_name:
                split_name = trimmed_name.split("/")
                # Special cases like split cards
                name_pt = split_name[0].strip()
                if len(split_name) > 2:
                    name_en = split_name[3].strip()
                else:
                    name_en = split_name[1].strip()
            else:
                name_pt = ""
                name_en = trimmed_name.strip()

            if name_en == response.meta['searched_card']:
                card['name'] = [name_pt, name_en]

                split_price = price.extract().strip().split("\n")

                price = split_price[0]
                quantity = split_price[1]
                # Get only the quantity number
                quantity_n = quantity[quantity.index('(') + 1:quantity.index(')')]

                card['price'] = price
                card['quantity'] = quantity_n

                card_list.append(card)

        if len(card_list) > 0:
            self.n_cards += 1
            # Add an empty card at the end of the list to add space between cards
            empty_card = Card()
            empty_card['name'] = ["", ""]
            empty_card['price'] = ""
            empty_card['quantity'] = ""
            card_list.append(empty_card)

        return card_list

    def parse(self, response):
        try:
            if not self.save_to:
                self.save_to = self.search_where + ".xlsx"

            cards = read_list_from_file(self.list_from)

            self.total_cards = len(cards)

            for card in cards:
                yield scrapy.Request(
                    url=self.search_url(card),
                    callback=self.search[self.search_where],
                    meta={'searched_card': card}
                )

        except AttributeError as e:
            logging.error(e)

        except KeyError as e:
            logging.error(e)






