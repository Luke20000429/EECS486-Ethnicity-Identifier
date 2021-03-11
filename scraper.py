from linkedin_scraper import Person, actions
from selenium import webdriver
import os

options = webdriver.ChromeOptions()
options.add_argument('–log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options,service_log_path=os.devnull)

email = "eecs486.proj.scraper@protonmail.com"
password = "shengenb"
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
person = Person("https://www.linkedin.com/in/strati-georgopoulos/", driver=driver)
print(person.name)



