import scrapy
from SpiderMTG.items import Auction


class AuctionSpider(scrapy.Spider):
    name = "auctions"
    base_url = 'https://www.ligamagic.com.br'
    start_urls = [
        'https://www.ligamagic.com.br/?view=leilao/listar&txt_user=PortoLivre',
    ]

    def _find_number_of_pages(self, response):
        last_page_href = response.xpath('//table[@cellpadding="1"]')[0]\
            .xpath('.//td[@width="16"]/a/@href').extract_first()

        n_pages = last_page_href.split("=")[-1]

        l = len(str(n_pages))

        next_page_href = last_page_href[:-len(str(n_pages))]

        return next_page_href, int(n_pages)

    def parse_auction(self, response):
        table = response.xpath(
            '//div[contains(@class,"Desktop")]'
            '//table[@class="tabela-interna sem-borda"]'
            '//tbody/'
            'tr/'
            'td')
        length = len(table)

        auction = response.meta['auction']

        if length < 6:
            pass
            # @TODO: Inform that it's not a card, it's a product
            # The card is a product
        else:
            n = length % 6
            quantity = table[0].xpath('.//p/b/text()').extract()
            card_pt = table[1].xpath('.//p/a/b/text()').extract()
            card_en = table[1].xpath('.//p/a/i/text()').extract()
            exp_pt = table[2].xpath('.//p/a/b/text()').extract()
            exp_en = table[2].xpath('.//p/a/i/text()').extract()
            language = table[3].xpath('.//p/text()').extract()
            condition = table[4].xpath('.//p/text()').extract()
            extra = table[5].xpath('.//p/font/b/text()').extract()

            # @TODO: Change to extract_first and remove the [0]
            auction['quantity'] = quantity[0]
            if len(card_en) > 0:
                auction['card'] = [card_pt[0], card_en[0]]
            else:
                auction['card'] = [card_pt[0]]
            if not exp_pt:
                auction['expansion'] = [exp_pt[0], exp_en[0]]
            else:
                auction['expansion'] = [exp_pt[0]]

            auction['language'] = language[0].replace(u'\xa0', '')
            auction['condition'] = condition[0]

            if len(extra) > 0:
                auction['extra'] = extra

        return auction

    def parse_auction_page(self, response):
        tables = response.xpath('//div[@class="boxshadow conteudo box-interna"]')

        if len(tables) == 3:
            # Ignore discount auctions
            auctions = tables[2].xpath(
                './/table[contains(@class,"Desktop")]/tbody/tr[contains(@id,"leilao")]')
        else:
            auctions = tables[1].xpath(
                './/table[contains(@class,"Desktop")]/tbody/tr[contains(@id,"leilao")]')

        for auction in auctions:
            a = Auction()
            title_and_href = auction.xpath('.//a[@class="big"]')
            a['title'] = title_and_href.xpath('.//text()').extract_first()
            a['href'] = self.base_url + title_and_href.xpath('.//@href').extract_first()[1:]
            a['price'] = auction.xpath('.//p[@class="lj b"]/text()').extract_first()
            a['bids'] = auction.xpath('.//a[@class="medium"]/i/text()').extract_first()
            time_left = auction.xpath('.//td[@class="txt-dir"]/a[@class="medium"]')
            # @TODO: See if this is necessary
            t = time_left.xpath('.//text()').extract_first()
            if t is None:
                t = time_left.xpath('.//font/text()').extract_first()

            a['time_left'] = t
            request = scrapy.Request(
                url=a['href'],
                callback=self.parse_auction,
                meta={'auction': a}
            )
            request.meta['auction'] = a
            yield request

    def parse(self, response):
        next_page_href, n_pages = self._find_number_of_pages(response)

        for i in range(1, 2):
            link = self.base_url + next_page_href + str(i)

            yield scrapy.Request(
                url=link,
                callback=self.parse_auction_page,
            )

