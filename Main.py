from SpiderMTG.spiders.auction_spider import AuctionSpider
from SpiderMTG.spiders.pricer import PricerSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import os


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(PricerSpider(), list_from="Zurgo.txt", search_where="mtgbr", save_to="go.xlsx")
    # process.crawl(AuctionSpider(settings))
    process.start()


if __name__ == "__main__":
    main()