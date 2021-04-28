from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import json

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options = chrome_options)
driver.get("https://www.mvideo.ru/")
driver.implicitly_wait(10)

#button_close = driver.find_element_by_xpath("//div[contains(@class, 'c-popup__close')]/span")
#button_close.click()
driver.execute_script("window.scrollTo(0, 1400);")

## Список словарей с полным описанием############################
items_info = []

## Список ссылок, для проверки повторений и конца каруселИ ###########################
items_links = []

while len(driver.find_elements_by_xpath("//ul[contains(@data-init-param, 'Новинки')]//li")) < 16:
    time.sleep(1)
    items = driver.find_elements_by_xpath("//ul[contains(@data-init-param, 'Новинки')]//li")

    for item in items:
        if item.find_element_by_xpath(".//h4/a").get_attribute('href') not in items_links:
            items_links.append(item.find_element_by_xpath(".//h4/a").get_attribute('href'))
            info_dict = {}
            info_dict['name'] = item.find_element_by_xpath(".//h4").text
            info_dict['link'] = item.find_element_by_xpath(".//h4/a").get_attribute('href')
            info_dict['price'] = json.loads(item.find_element_by_xpath(".//h4/a").get_attribute('data-product-info'))['productPriceLocal']
            info_dict['category'] = json.loads(item.find_element_by_xpath(".//h4/a").get_attribute('data-product-info'))['productCategoryName']
            info_dict['vendor'] = json.loads(item.find_element_by_xpath(".//h4/a").get_attribute('data-product-info'))['productVendorName']
            items_info.append(info_dict)

    next_button = driver.find_element_by_xpath("//ul[contains(@data-init-param, 'Новинки')]/..//..//a[contains(@class, 'next-btn')]")
    next_button.click()

print(f'Товаров в разделе "Новинки": {len(items_info)}')

## Добавление в БД ##################################################################
client = MongoClient('127.0.0.1', 27017)
db = client['items_db']
items_list = db.items_list
items_list.delete_many({})

items_list.insert_many(items_info)
print(f'Товаров добавлено в БД: {items_list.count_documents({})}')