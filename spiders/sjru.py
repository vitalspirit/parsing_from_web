import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&noGeo=1']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//div[@class='f-test-search-result-item']//a[contains(@href, 'vakansii')]/@href").extract()
        next_page = response.css("a.f-test-link-Dalshe::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css("h1::text").extract_first()
        salary = response.xpath("//span[contains(@class, 'ZON4b')]/span").extract()
        link = response.url
        domain = self.allowed_domains
        yield JobparserItem(name=name, salary=salary, link=link, domain=domain)