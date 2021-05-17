import requests
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('rabota_by', 'dev_by')
# обход блокировки сайта на скрапинг данных с него
headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/49.0.2623.112 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
           ]


def rabota_by(url, city=None, language=None):
    """Парсинг на сайте rabota.by"""

    resp = requests.get(url, headers=headers[randint(0, 2)])
    jobs = []
    errors = []  # отлов ошибок парсера, потому что могут поменять названия
    if url:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', class_='vacancy-serp')
            if main_div:
                div_list = main_div.find_all('div', class_='vacancy-serp-item')
                for div in div_list:
                    href = div.find('span', class_='g-user-content').a['href']
                    title = div.find('span', class_='g-user-content').a.text
                    company = div.find('div', class_='vacancy-serp-item__meta-info-company').a.text
                    description = div.find('div', class_='g-user-content').text
                    description = description.replace('<highlighttext>', '').replace('</highlighttext>', '')
                    jobs.append({'title': title, 'url': href, 'company': company, 'description': description,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response', 'error': resp.status_code})

    return jobs, errors


def dev_by(url, city=None, language=None):
    """Парсинг на сайте dev.by"""

    domain = 'https://jobs.dev.by'
    resp = requests.get(url, headers=headers[randint(0, 2)])
    jobs = []
    errors = []  # отлов ошибок парсера, потому что могут поменять названия
    if url:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', class_='vacancies-list__body')
            if main_div:
                premium_div_list = soup.find_all('div', class_='vacancies-list-item premium-vacancy')
                marked_div_list = soup.find_all('div', class_='vacancies-list-item vacancies-list-item--marked')
                for div in premium_div_list:
                    title_block = div.find('a', class_='vacancies-list-item__link_block')
                    href = domain + title_block.get('href')
                    title = title_block.find('div', class_='premium-vacancy__title').text
                    company = div.find('div', class_='premium-vacancy__footer').a.text
                    description = div.find('div', class_='premium-vacancy__row').next_sibling.text
                    jobs.append({'title': title, 'url': href, 'company': company, 'description': description,
                                 'city_id': city, 'language_id': language})
                for div in marked_div_list:
                    title_block = div.find('a', class_='vacancies-list-item__link_block')
                    href = domain + title_block.get('href')
                    title = title_block.text
                    company = div.find('a', class_='js-vacancy__footer__company-name').text
                    description_divs = div.find_all('div', class_='vacancies-list-item__technology-tag__name')
                    description_list = [x.text for x in description_divs]
                    description = ' '.join(description_list)
                    jobs.append({'title': title, 'url': href, 'company': company, 'description': description,
                                 'city_id': city, 'language_id': language})

                soup1 = BS(resp.content, 'html.parser')  # очистка данных от лишнего

                removals1 = soup1.find_all('div', class_='vacancies-list-item premium-vacancy')
                for rem1 in removals1:
                    rem1.decompose()
                removals2 = soup1.find_all('div', class_='vacancies-list-item vacancies-list-item--marked')
                for rem2 in removals2:
                    rem2.decompose()
                removals3 = soup1.find_all('div', class_='vacancies-item-banner')
                for rem3 in removals3:
                    rem3.decompose()
                removals4 = soup1.find_all('div', class_='vacancies-list-item__body important-block important-block_hint')
                for rem4 in removals4:
                    rem4.decompose()
                div_list = soup1.find_all('div', class_='vacancies-list-item__body js-vacancies-list-item--open')

                for div in div_list:
                    title_block = div.find('a', class_='vacancies-list-item__link_block')
                    href = domain + title_block.get('href')
                    title = title_block.text
                    company = div.find('div', class_='vacancies-list-item__company').text
                    company = company.replace('Удалённо', '')
                    jobs.append({'title': title, 'url': href, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response', 'error': resp.status_code})

    return jobs, errors
