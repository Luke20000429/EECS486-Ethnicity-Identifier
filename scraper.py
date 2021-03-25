# from linkedin_scraper import Person, actions
from selenium import webdriver
import os
from bs4 import BeautifulSoup as BS
from webHandler import login

limit = 10

def search(url, driver, urls, connections):

    if len(connections) < limit:

        driver.get('https://www.linkedin.com' + url)
        html = driver.page_source
        soup = BS(html, 'html.parser')

        name = soup.find('li', class_="inline t-24 t-black t-normal break-words")
        nation = soup.find('li', class_="t-16 t-black t-normal inline-block")
        name = name.string.replace(" ", "").replace("\n", "")
        nation = nation.string.replace(" ", "").replace("\n", "")
        nation = nation[nation.rfind(',')+1 : ]
        print(name + "-" + nation)
        connections.append((name, nation))

        for connection in soup.find_all('a', class_="ember-view pv-browsemap-section__member align-items-center"): # find possible connection
            link = connection['href']
            print(link)
            if link not in urls:
                urls.append(link)
                print(link)

    return urls, connections

def main():

    email = "eecs486.proj.scraper@protonmail.com"
    password = "shengenb"

    print("logining in...")
    print("this could take some time...")
    driver = login(email, password) # if email and password isnt given, it'll prompt in terminal
    print("successfully login!")

    # print("start getting")
    # driver.get("https://www.linkedin.com/feed/")
    # print("got!")
    connections = list()
    urls = []
    html = driver.page_source
    soup = BS(html, 'html.parser')
    # with open('linkedin.html', 'w', encoding='utf-8') as f:
        # f.write(html)
    
    for connection in soup.find_all('a', class_="ember-view pv-browsemap-section__member align-items-center"): # find possible connection
        link = connection['href']
        if link not in urls:
            urls.append(link)
            print(link)

    
    idx = 0

    print("start crawling...")

    while len(connections) < limit:
        urls, connections = search(urls[idx], driver, urls, connections)
        idx += 1

    # for connection in soup.find_all('a', class_="ember-view pv-browsemap-section__member align-items-center"): # find possible connection
        # print(connection['href'])


if __name__ == '__main__':
    main()
    



