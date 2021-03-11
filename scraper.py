from linkedin_scraper import Person, actions
from selenium import webdriver
import os
from bs4 import BeautifulSoup as BS

options = webdriver.ChromeOptions()
options.add_argument('–log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options,service_log_path=os.devnull)

email = "eecs486.proj.scraper@protonmail.com"
password = "shengenb"
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
print("start getting")
driver.get("https://www.linkedin.com/in/xueshen-liu-a75718205/")
print("got!")

html = driver.page_source
soup = BS(html, 'html.parser')
with open('linkedin.html', 'w', encoding='utf-8') as f:
    f.write(html)

for connection in soup.find_all('a', class_="ember-view pv-browsemap-section__member align-items-center"):
    print(connection['href'])

# person = Person("https://www.linkedin.com/in/strati-georgopoulos/", driver=driver)

# print(person.contacts)



