import requests
from bs4 import BeautifulSoup as BS

#from scraping.models import Language, City

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',    #обход блокировки сайта на скрапинг данных с него
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

#https://rabota.by/search/vacancy?clusters=true&area=1002&no_magic=true&enable_snippets=true&salary=&st=searchVacancy&text=Python
#https://jobs.dev.by/?&filter[search]=python%20

lang = 'Javascript' #Language.slug.capitalize()

def rabota_by(url):

    '''Парсинг на сайте rabota.by для языка Python и города Минск'''

    resp = requests.get(url, headers=headers)
    jobs = []
    errors = []           #отлов ошибок парсера, потому что могут поменять названия
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', class_='vacancy-serp')
        if main_div:
            div_list = main_div.find_all('div', class_='vacancy-serp-item')
            for div in div_list:
                href = div.find('span', class_='g-user-content').a['href']
                title = div.find('span', class_='g-user-content').a.text
                company = div.find('div', class_='vacancy-serp-item__meta-info-company').a.text
                description = div.find('div', attrs={'data-qa': "vacancy-serp__vacancy_snippet_responsibility"}).text + \
                              div.find('div', attrs={'data-qa': "vacancy-serp__vacancy_snippet_requirement"}).text
                #language = div.find('div', attrs={'data-qa': "vacancy-serp__vacancy_snippet_responsibility"}).text
                jobs.append({'title': title, 'url': href, 'company': company, 'description': description})
        else:
            errors.append({'url': url, 'title': 'Div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response', 'error': resp.status_code})

    return jobs, errors


def dev_by(url):

    '''Парсинг на сайте dev.by для языка Python и города Минск'''
    domain = 'https://jobs.dev.by'
    resp = requests.get(url, headers=headers)
    jobs = []
    errors = []  # отлов ошибок парсера, потому что могут поменять названия
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', class_='vacancies-list__body')
        if main_div:
            premium_div_list = main_div.find_all('div', class_='vacancies-list-item premium-vacancy')
            div_list = main_div.find_all('div', class_='vacancies-list-item vacancies-list-item--marked')
            for div in premium_div_list:
                title_block = div.find('a', class_='vacancies-list-item__link_block')
                href = domain + title_block.get('href')
                title = title_block.find('div', class_='premium-vacancy__title').text
                company = div.find('div', class_='premium-vacancy__footer').a.text
                description = div.find('div', class_='premium-vacancy__row').next_sibling.text
                jobs.append({'title': title, 'url': href, 'company': company, 'description': description})
            for div in div_list:
                title_block = div.find('a', class_='vacancies-list-item__link_block')
                href = domain + title_block.get('href')
                title = title_block.text
                company = div.find('a', class_='js-vacancy__footer__company-name').text
                description_divs = div.find_all('div', class_='vacancies-list-item__technology-tag__name')
                description_list = [x.text for x in description_divs]
                description = ' '.join(description_list)
                jobs.append({'title': title, 'url': href, 'company': company, 'description': description})
        else:
            errors.append({'url': url, 'title': 'Div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response', 'error': resp.status_code})

    return jobs, errors


if __name__ == '__main__':
    url = 'https://rabota.by/search/vacancy?clusters=true&area=1002&no_magic=true&enable_snippets=true&salary=&st=searchVacancy&text=Python'
    jobs, errors = rabota_by(url)
    h = open('work.txt', 'w')
    h.write(str(jobs))
    h.close()