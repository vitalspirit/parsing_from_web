from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient
import datetime

client = MongoClient('127.0.0.1', 27017)
db = client['news_db']
news = db.news
news.delete_many({})

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}

url_1 = 'https://lenta.ru'
url_2 = 'https://news.mail.ru'

news_list = []

# Работа с mail.ru ##############################################
response = requests.get(url_2)
dom = html.fromstring(response.text)

articles = dom.xpath("//div[@class='daynews__item'] | //li[@class='list__item'] | //span[@class='cell']")

for article in articles:
    news_dic = {}
    link = article.xpath(".//a//@href")[0]
    title = " ".join(article.xpath(".//span[contains(@class, 'js-topnews__notification')]/text() | .//a//text()")).replace("\xa0", " ")
    source = url_2
    date = str(datetime.date.today())

    news_dic['date'] = date
    news_dic['title'] = title
    news_dic['link'] = link
    news_dic['source'] = source

    news_list.append(news_dic)




# Работа с lenta.ru ##############################################
response = requests.get(url_1)
dom = html.fromstring(response.text)

articles = dom.xpath("//div[@class='item']")

for article in articles:
    news_dic = {}
    title = "".join(article.xpath(".//a/text()")).replace("\xa0", " ")
    link = article.xpath("./a/@href")[0]
    date = link.split("/")[4] + "/" + link.split("/")[3] + "/" + link.split("/")[2]
    source = url_1
    abs_link = url_1 + link

    news_dic['date'] = date
    news_dic['title'] = title
    news_dic['link'] = abs_link
    news_dic['source'] = source

    news_list.append(news_dic)


pprint(news_list)
news.insert_many(news_list)
print(news.count_documents({}))