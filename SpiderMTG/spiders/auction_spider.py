import scrapy
from SpiderMTG.items import Auction


class AuctionSpider(scrapy.Spider):
    name = "auctions"
    start_urls = [
        'https://www.ligamagic.com.br/?view=leilao/listar&txt_user=PortoLivre',
    ]

    def parse_auction(self, response):
        table = \
            response.xpath('//div[contains(@class,"Desktop")]//table[@class="tabela-interna sem-borda"]//tbody/tr/td')
        length = len(table)
        self.log("Length: " + str(length))

        auction = response.meta['auction']

        if length < 6:
            pass
            # The card is a product
        else:
            # self.log(table[0].extract())
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

    def parse(self, response):
        self.log("Accessing: " + response.url)
        # Get all current auctions
        self.log("Getting Titles")
        title_and_href = response.xpath('//table[contains(@class,"Desktop")]//a[@class="big"]')
        self.log("Getting Prices")
        prices_and_bids = response.xpath('//td[@class="double txt-dir"]')
        self.log("Getting Time Left")
        time_left = response.xpath('//td[@class="txt-dir"]/a[@class="medium"]')

        for th, pb, tl in zip(title_and_href, prices_and_bids, time_left):
            a = Auction()
            a['title'] = th.xpath('.//text()').extract_first()
            a['href'] = th.xpath('.//@href').extract_first()[1:]
            a['price'] = pb.xpath('.//p[@class="lj b"]/text()').extract_first()
            a['bids'] = pb.xpath('.//a[@class="medium"]/i/text()').extract_first()
            a['time_left'] = tl.xpath('.//text()').extract_first()
            request = scrapy.Request("https://www.ligamagic.com.br" + a['href'], callback=self.parse_auction,
                                     meta={'auction': a})
            request.meta['auction'] = a
            yield request
