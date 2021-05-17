from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from pprint import pprint

from otparser.spiders.otru import OtruSpider
from otparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # query = input('')
    process.crawl(OtruSpider, query='радиатор')

    process.start()