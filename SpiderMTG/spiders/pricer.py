import scrapy


class PricerSpider(scrapy.Spider):
    name = "pricer"
    base_url = 'https://www.ligamagic.com.br'
    start_urls = [
        'https://www.ligamagic.com.br/?view=leilao/listar&txt_user=PortoLivre',
    ]

    def parse(self, response):
        pass
