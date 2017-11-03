from SpiderMTG.spiders.auction_spider import AuctionSpider
from SpiderMTG.spiders.pricer import PricerSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import os


def main():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    settings = get_project_settings()

    process.crawl(PricerSpider(settings), list_from="Zurgo.txt")
    # process.crawl(AuctionSpider(settings))
    process.start()


if __name__ == "__main__":
    main()