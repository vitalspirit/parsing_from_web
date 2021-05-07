 # Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy080421

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        salary_max = None
        vacancy_info = {}
        vacancy_info['salary_max'] = None
        vacancy_info['salary_min'] = None
        vacancy_info['name'] = item['name']
        vacancy_info['link'] = item['link']
        vacancy_info['domain'] = spider.allowed_domains[0]

        if spider.name == "hhru":
            if ' до ' in item['salary']:
                vacancy_info['salary_max'] = item['salary'][item['salary'].index(' до ')+1].replace("\xa0", "")
            if 'от ' in item['salary']:
                vacancy_info['salary_min'] = item['salary'][item['salary'].index('от ') + 1].replace("\xa0", "")
        else:

            if item['salary'][0].find("от") > 0:
                vacancy_info['salary_min'] = item['salary'][0][item['salary'][0].find("от")+19:item['salary'][0].find("/")-2]
                vacancy_info['salary_max'] = item['salary'][0]
            elif item['salary'][0].find(">до<") > 0:
                vacancy_info['salary_min'] = item['salary'][0]
                vacancy_info['salary_max'] = item['salary'][0][item['salary'][0].find(">до<")+20:item['salary'][0].find("/")-2]
            elif item['salary'][0].find(">—<") > 0:
                vacancy_info['salary_min'] = re.search(r'>[0-9]+\s[0-9]+', item['salary'][0])
                vacancy_info['salary_max'] = item['salary'][0]

        print(vacancy_info)
        collection.insert_one(vacancy_info)
        return item


