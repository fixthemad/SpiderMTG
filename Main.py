from SpiderMTG.spiders.auction_spider import AuctionSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    settings = get_project_settings()
    process.crawl(AuctionSpider(settings))
    process.start()

if __name__ == "__main__":
    main()