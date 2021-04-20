from bs4 import BeautifulSoup as bs
import requests

main_url = 'http://hh.ru'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}

vacancies=[]

# ПОЛУЧЕНИЕ ДАННЫХ О ЗАРПЛАТАХ ##############################################################################
def salary(vacancy_salary):
    if vacancy_salary:
        vacancy_salary_min = 'None'
        vacancy_salary_max = 'None'
        vacancy_salary_currency = 'None'

        if 'от' in vacancy_salary.getText().split():
            if vacancy_salary.getText().split()[2].isdecimal() == True:
                vacancy_salary_min = int(vacancy_salary.getText().split()[1] + vacancy_salary.getText().split()[2])
            else:
                vacancy_salary_min = int(vacancy_salary.getText().split()[1])
        elif '–' in vacancy_salary.getText().split():
            vacancy_salary_min = int("".join(vacancy_salary.getText()[0:vacancy_salary.getText().index('–') - 1].split()))
            if vacancy_salary.getText()[vacancy_salary.getText().index('–') + 1:].split()[1].isdecimal() == True:
                vacancy_salary_max = int(vacancy_salary.getText()[vacancy_salary.getText().index('–') + 1:].split()[0] +
                                         vacancy_salary.getText()[vacancy_salary.getText().index('–') + 1:].split()[1])
            else:
                vacancy_salary_max = int(vacancy_salary.getText()[vacancy_salary.getText().index('–') + 1:].split()[0])
        elif 'до' in vacancy_salary.getText().split():
            vacancy_salary_max = int(vacancy_salary.getText().split()[1] + vacancy_salary.getText().split()[2])

        if vacancy_salary.getText().endswith('руб.'):
            vacancy_salary_currency = "руб."
        elif vacancy_salary.getText().endswith('USD'):
            vacancy_salary_currency = "USD"
        else:
            vacancy_salary_currency = "None"

    else:
        vacancy_salary_min = 'None'
        vacancy_salary_max = 'None'
        vacancy_salary_currency = 'None'
    return vacancy_salary_min, vacancy_salary_max, vacancy_salary_currency


text = input('Пожалйста введите текст для поиска вакансий')



# ЗАГРУЗКА ДАННЫХ О ВАКАНСИЯХ С САЙТА ########################################################
def downloading ():
    page = 0
    while page != 'finish':
        params = {'clusters': 'true',
                  'enable_snippets': 'true',
                  'text': text,
                  'L_save_area': 'true',
                  'area': '113',
                  'showClusters': 'true',
                  'page': page
                  }

        response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)
        dom = bs(response.text, 'html.parser')
        vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item'})

        for vacancy in vacancy_list:
            vacancy_data = {'vacancy_source': 'hh.ru'}
            vacancy_name = vacancy.find('a', {'class': 'bloko-link'}).getText()
            vacancy_link = vacancy.find('a', {'class': 'bloko-link'})['href']
            vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            vacancy_salary_min = salary(vacancy_salary)[0]
            vacancy_salary_max = salary(vacancy_salary)[1]
            vacancy_salary_currency = salary(vacancy_salary)[2]
            _id = vacancy_link.split('/')[-1]

            vacancy_data['id'] = _id
            vacancy_data['vacancy_name'] = vacancy_name
            vacancy_data['vacancy_salary_min'] = vacancy_salary_min
            vacancy_data['vacancy_salary_max'] = vacancy_salary_max
            vacancy_data['vacancy_salary_currency'] = vacancy_salary_currency
            vacancy_data['vacancy_link'] = vacancy_link

            vacancies.append(vacancy_data)

        if dom.find('a', {'data-qa': 'pager-next'}):
            page += 1
        else:
            page = "finish"

        print(f'Страница {page} обработана, вакансии добавлены в список. В списке {len(vacancies)} вакансий')
    print(vacancies)



downloading()
### Урок №3 - Домашнее задание ##############################################################

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['vacancy_db']

vacancy_list = db.vacancy_list
vacancy_list.delete_many({})

#vacancy_list.insert_many(vacancies)


# Добавление записей в БД или обновление имеющихся #########################################
def updating(item) :
    if vacancy_list.count_documents({'id': item['id']}) > 0:
        vacancy_list.update_one({'id': item['id']}, {'$set' : item})
        pass
    else:
        vacancy_list.insert_one(item)

for rec in vacancies:
    updating(rec)

# Создаем список валют #######

currency_list = []

for i in vacancies:
    if i['vacancy_salary_currency'] not in currency_list:
        currency_list.append(i['vacancy_salary_currency'])
    else:
        pass
currency_list.remove('None')



desired = input("Пожалуйста введите желаемую заработную плату")
print("Пожалуйста выберите валюту")
for i in currency_list:
    print(f'{i} - цифра {currency_list.index(i)}')
curr = int(input("?"))


## Поиск вакансий по ЗП #########################################################################
counter = 0
for vacancy in vacancy_list.find({'$or': [{'vacancy_salary_min': {'$lte': desired}},
                                          {'vacancy_salary_max': {'$gte': desired}}]
                                 }):

    if vacancy['vacancy_salary_currency'] == currency_list[curr]:
        counter += 1
        pprint(vacancy)


print (f' Всего вакансий подходит: {counter}')

## Добавление новых вакансий ####################################################################

