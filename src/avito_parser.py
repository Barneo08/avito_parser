import os
import time

import undetected_chromedriver as uc
from datetime import datetime, timedelta
from src.helpers import transliterate, aslocaltimestr
from src.locator import LocatorAvito
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.window import WindowTypes
from random import choice, randint


class AvitoParser:
    def __init__(self,
                 request: str,
                 base_url: str = 'https://www.avito.ru/',
                 pages_count: int = 1,
                 ads_count: int = 5,
                 city: str = 'all',
                 version_main=None,
                 use_proxy=False):
        self.base_url = base_url
        self.request = request
        self.pages_count = pages_count
        self.ads_count = ads_count
        if city != 'all':
            self.city = transliterate(city)
        else:
            self.city = city
        self.version_main = version_main
        self.use_proxy = use_proxy
        self.page_data_list = []
        self.url = base_url + self.city + '?q=' + request
        self.page_url_list = []

    def __set_up(self):
        options = Options()
        options.add_argument('--headless')
        _ua = choice(list(map(str.rstrip, open(os.path.join('src', 'user_agent_pc.txt')).readlines())))
        options.add_argument(f'--user-agent={_ua}')
        """----------------Настройка прокси-------------"""
        if self.use_proxy:
            proxy_server_url = choice(list(map(str.rstrip, open(os.path.join('src', 'proxy_list.txt')).readlines())))
            options.add_argument(f'--proxy-server={proxy_server_url}')
        """---------------------------------------------"""
        self.driver = uc.Chrome(version_main=114,
                                options=options,
                                )

    def __get_url(self):
        self.driver.get(self.url)

    def __paginator(self):
        """Кнопка далее"""
        while self.pages_count > 0:
            self.__parse_ads_page_url()
            """Проверяем есть ли кнопка далее"""
            if self.driver.find_elements(*LocatorAvito.NEXT_BTN):
                self.driver.find_element(*LocatorAvito.NEXT_BTN).click()
                self.pages_count -= 1
            else:
                break

    def __parse_ads_page_url(self):
        ads = self.driver.find_elements(*LocatorAvito.ADS)
        for ad in ads:
            url = ad.find_element(*LocatorAvito.URL).get_attribute("href")
            self.page_url_list.append(url)

    def parse_urls_list(self):
        try:
            self.__set_up()
            self.__get_url()
            self.__paginator()
        except Exception as error:
            print('Ошибка {}'.format(error))
        finally:
            return self.page_url_list

    def parse_ads_page(self, url: str):
        months_dict = {
            'января': '01',
            'февраля': '02',
            'марта': '03',
            'апреля': '04',
            'мая': '05',
            'июня': '06',
            'июля': '07',
            'августа': '08',
            'сентября': '09',
            'октября': '10',
            'ноября': '11',
            'декабря': '12',
        }

        data = dict()
        #self.driver.switch_to.new_window(WindowTypes.TAB)  # Открываем в новой вкладке
        self.__set_up()
        self.driver.get(url)
        #self.driver.switch_to.window(self.driver.window_handles[1])

        """Номер объявления"""
        if self.driver.find_elements(*LocatorAvito.AD_ID):
            ad_id = self.driver.find_element(*LocatorAvito.AD_ID).text.split()[1]
            data["ad_id"] = int(ad_id)

        """Название"""
        if self.driver.find_elements(*LocatorAvito.NAME):
            name = self.driver.find_element(*LocatorAvito.NAME).text
            data["name"] = name

        """Цена"""
        if self.driver.find_elements(*LocatorAvito.PRICE):
            price = self.driver.find_element(*LocatorAvito.PRICE).text.replace('\n', '').split(' или')[0]
            data["price"] = price

        """Адрес"""
        if self.driver.find_elements(*LocatorAvito.ADDRESS):
            address = self.driver.find_element(*LocatorAvito.ADDRESS).text#.replace('\n', ' ')
            data["address"] = address

        """Описание. Первые 9 символов: Описание\n"""
        if self.driver.find_elements(*LocatorAvito.DESCRIPTIONS):
            descriptions = self.driver.find_element(*LocatorAvito.DESCRIPTIONS).text
            data["descriptions"] = descriptions

        """Дата публикации"""
        if self.driver.find_elements(*LocatorAvito.DATE_PUBLIC):
            date_public = self.driver.find_element(*LocatorAvito.DATE_PUBLIC).text
            if "· " in date_public:
                date_public = date_public.replace("· ", '')
            date_public = date_public.split()
            if 'сегодня' in date_public:
                date_public = '{} {}'.format(aslocaltimestr(datetime.utcnow())[:-6], date_public[2])
            elif 'вчера' in date_public:
                date_public = '{} {}'.format(aslocaltimestr(datetime.utcnow() - timedelta(days=1))[:-6], date_public[2])
            else:
                date_public = '2023-{}-{} {}'.format(months_dict[date_public[1]], date_public[0], date_public[3])
            data["date_public"] = date_public

        """Количество просмотров"""
        if self.driver.find_elements(*LocatorAvito.TOTAL_VIEWS):
            total_views = self.driver.find_element(*LocatorAvito.TOTAL_VIEWS).text.split()[0]
            data["views"] = total_views

        """Проверка на закрытость страницы"""
        if self.driver.find_elements(*LocatorAvito.CLOSED):
            data["is_closed"] = True
        else:
            data["is_closed"] = False

        """URL"""
        data['url'] = url
        """Город"""
        data['city'] = url.split('/')[3]
        """Закрывает вкладку №2 и возвращается на №1"""
        self.driver.close()
        #self.driver.switch_to.window(self.driver.window_handles[0])

        print(data)
        return data

    def __save_data(self, data: dict):
        """Пока эта заглушка. ПОТОМ ПЕРЕДЕЛАТЬ С СОХРАНЕНИЕМ В SQLite"""
        pass

    def parse_pages_from_url_list(self):
        data_list = []
        try:
            for index, url in enumerate(self.parse_urls_list()):
                time.sleep(randint(5, 10))
                data_list.append(self.parse_ads_page(url))
                # print(self.parse_ads_page(url))
                """---без прокси часто вылетает 429, поэтому парсим только первые ads_count записей---"""
                if index == self.ads_count - 1:
                    return data_list
                """--------------------"""
        except Exception as error:
            print('Ошибка {}'.format(error))
        finally:
            self.driver.quit()
            return data_list
