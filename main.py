import cloudscraper
import re
from bs4 import BeautifulSoup

params = {
    'forceLocation': False,
    'locationId': 653040,
    'lastStamp': 1683748131,
    'limit': 30,
    'offset': 89,
    'categoryId': 4
}


def get_html(url, params=None):
    s = cloudscraper.create_scraper(
        delay=10,
        browser={
            'custom': 'ScraperBot/1.0'
        }
    )
    request = s.get(url, params=params)
    return request


def get_pages_count(html):
    soup = BeautifulSoup(html, features='html.parser')
    try:
        # Находим номер последней страницы с помощью тега span
        # Пример вывода pages: <span class="styles-module-text-InivV">100</span>
        pages = soup.find('div', class_='js-pages pagination-pagination-_FSNE') \
            .find_all('span', class_=re.compile('styles-module-text'))[-1]
        total_pages = str(pages)
        # Забираем число найдя индексы открывающего и закрывающего тега в строке
        total_pages = total_pages[total_pages.find('>') + 1:total_pages.rfind('<')]
        return int(total_pages)
    except AttributeError:
        print('Ошибка парсера')


#def get_page_data(html):
url = 'https://www.avito.ru/all?p=1&q=котик'

html = get_html(url)

soup = BeautifulSoup(html.text, features='html.parser')
ads = soup.find('div', class_=re.compile('items-items'))
print(ads)

'''
def main():
    base_url = 'https://www.avito.ru/all?'
    page_part = 'p='
    query_part = 'q='
    query = 'Котик'
    #query = input('Введите запрос: ')

    print(base_url + query_part + query)
    html = get_html(base_url + query_part + query)
    print(html)
    # total_pages = get_pages_count(html.text)

    total_pages = 2

    for i in range(1, total_pages + 1):
        url_page = base_url + page_part + f'{i}&' + query_part + query
        html = get_html(url_page)
        page_data = get_page_data(html)
        print(page_data)


if __name__ == '__main__':
    main()
'''