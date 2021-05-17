import scrapy
from scrapy.http import HtmlResponse
from otparser.items import OtparserItem
from scrapy.loader import ItemLoader

class OtruSpider(scrapy.Spider):
    name = 'otru'
    allowed_domains = ['leroymerlin.ru']


    def __init__(self, query):
        super(OtruSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        goods_links = response.xpath("//a[@data-qa='product-name']")
        next_page = response.xpath("//a[contains(@aria-label, 'Следующая страница')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in goods_links:
            yield response.follow(link, callback=self.pasrse_goods)






    def pasrse_goods(self, response:HtmlResponse):
        loader = ItemLoader(item=OtparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('photos', "//a[@class='image']/uc-image/img/@src | //picture[@id='picture-box-id-generated-0']/img/@src")
        loader.add_xpath('price', "//span[@slot = 'price']/text()")

        full_details = {}
        full_list = response.xpath("//div[@class='def-list__group']")
        for item in full_list:
            name = item.css("dt::text").extract_first().strip()
            value = item.css("dd::text").extract_first().strip()
            full_details[name] = value
        print()

        loader.add_value('details', full_details)
        loader.add_value('link', response.url)
        yield loader.load_item()







        # name = response.xpath("//h1/text()").extract_first()
        # photos = response.xpath("//img[@class='displayedItem__images__thumbImage']/@src").extract()
        # if not photos:
        #     photos = response.xpath("//img[@id='popupCatalogItem_bigImage']/@src").extract()
        # yield OtparserItem(name=name, photos=photos)