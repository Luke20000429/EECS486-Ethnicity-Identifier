import threading
from bs4 import BeautifulSoup
import requests


def scrape_nation_dict():
    nation_dict = {}
    nation_dict_url = 'http://www.olympedia.org/countries'
    response = requests.get(
                nation_dict_url, headers={'user-agent': 'patchekh'})
    Parser = BeautifulSoup(response.text, 'html.parser')
    new_hrefs = Parser.find_all('td')
    for td in new_hrefs:
        if td.contents and len(td.contents[0].contents) == 1:
            nation_dict[td.contents[0].get('href')[-3:]] = td.contents[0].contents[0]

    with open("NationDict.txt", 'w') as f:
        for nation in nation_dict:
            f.write(nation + '\t' + nation_dict[nation] + '\n')

def scrape_olympics(url_list, athlete_nationality_dict):
    for url in url_list:
        response = requests.get(
                url, headers={'user-agent': 'patchekh'})
        Parser = BeautifulSoup(response.text, 'html.parser')
        new_hrefs = Parser.find_all('td')
        i = 0
        while i < len(new_hrefs) - 1:
            # print(new_hrefs[i].contents)
            if len(new_hrefs[i]) != 3 or not new_hrefs[i].contents[1].get('href'):
                i += 1
                continue
            athlete = new_hrefs[i].contents[1].contents[0]
            if athlete in athlete_nationality_dict:
                i += 1
                continue
            i += 1
            athlete_nationality_dict[athlete] = []
            if new_hrefs[i].contents:
                for elem in new_hrefs[i].contents[0].contents:
                    if len(elem) == 3:
                        athlete_nationality_dict[athlete].append(elem)
                
            i += 1

def main():
    init_list_url = 'http://www.olympedia.org/lists'
    response = requests.get(
                init_list_url, headers={'user-agent': 'patchekh'})
    Parser = BeautifulSoup(response.text, 'html.parser')
    new_hrefs = Parser.find_all('a')
    url_list = []
    for href in new_hrefs:
        link = href.get('href')
        if '/lists' in link and '/manual' in link:
            url_list.append(init_list_url.rstrip('/lists') + link)
         
    athlete_nationality_dict = {}   
    
    thread_1 = threading.Thread(target=scrape_olympics, args=(url_list[:len(url_list) // 4], athlete_nationality_dict))
    thread_2 = threading.Thread(target=scrape_olympics, args=(url_list[len(url_list) // 4 : len(url_list) // 4 * 2], athlete_nationality_dict))
    thread_3 = threading.Thread(target=scrape_olympics, args=(url_list[len(url_list) // 4 * 2 :len(url_list) // 4 * 3], athlete_nationality_dict))
    thread_4 = threading.Thread(target=scrape_olympics, args=(url_list[len(url_list) // 4 * 3:], athlete_nationality_dict))
    
    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_4.start()
    
    thread_1.join()
    thread_2.join()
    thread_3.join()
    thread_4.join()
            
    with open("NameNationality.txt", 'w') as f:
        for athelete in athlete_nationality_dict:
            f.write(athelete + '\t')
            for nation in athlete_nationality_dict[athelete]:
                f.write(nation + ' ')
            f.write('\n')
      
    scrape_nation_dict()

if __name__ == '__main__':
    main()
