import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css("h1::text").extract_first()
        salary = response.css("p.vacancy-salary span::text").extract()
        link = response.url
        domain = self.allowed_domains
        yield JobparserItem(name=name, salary=salary, link=link, domain=domain)

