from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

driver = webdriver.Chrome()
driver.get("http://www.mail.ru")
driver.implicitly_wait(10)

login = driver.find_element_by_name("login")
login.send_keys("karina_school40@mail.ru")
button = driver.find_element_by_xpath("//button[@data-testid='enter-password']")
button.click()
password = driver.find_element_by_name("password")
password.send_keys('neutrino15@')
button = driver.find_element_by_xpath("//button[@data-testid='login-to-mail']")
button.click()


### Получение списка ссылок на все письма ################################################
link_list = []
the_last_letter = False

while not the_last_letter:
    time.sleep(4)
    list = driver.find_elements_by_xpath("//a[contains(@class, 'js-letter-list-item')]")
    for item in list:
        link = item.get_attribute('href')
        if link not in link_list:
            link_list.append(link)
        else:
            the_last_letter = True
    actions = ActionChains(driver)
    actions.move_to_element(list[-1])
    actions.perform()

print(f'Ссылки на {len(link_list)} писем собраны')


### Получение информации по каждому письму ################################################
full_info = []
for link in link_list:
    mail_info = {}
    driver.get(link)
    driver.implicitly_wait(10)
    author = driver.find_element_by_xpath("//span[contains(@class, 'letter-contact')]").get_attribute('title')
    date = driver.find_element_by_class_name("letter__date").text
    theme = driver.find_element_by_xpath("//h2[@class='thread__subject']").text
    text =  driver.find_element_by_class_name("letter__body").text

    mail_info["from"] = author
    mail_info["date"] = date
    mail_info["theme"] = theme
    mail_info["text"] = text

    full_info.append(mail_info)

print(len(full_info))

## Добавление в БД ##################################################################
client = MongoClient('127.0.0.1', 27017)
db = client['mail_db']
mail_list = db.mail_list
mail_list.delete_many({})

mail_list.insert_many(full_info)
print(mail_list.count_documents({}))