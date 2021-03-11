from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import os


def login(email, password):

    options = webdriver.ChromeOptions()
    options.add_argument('–log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options,service_log_path=os.devnull)

    driver.get("https://www.linkedin.com/login")
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    email_elem = driver.find_element_by_id("username")
    email_elem.send_keys(email)

    password_elem = driver.find_element_by_id("password")
    password_elem.send_keys(password)
    password_elem.submit()

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-nav-item")))

    return driver