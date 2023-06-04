### avito_parser

Задача: разработать парсер объявлений сайта авито с кешем поисковых запросов в БД SQLite

На текущий момент программа работает следующим образом:
1) Получает на вход поисковый запрос и город поиска(если оставить это поле пустым, то программа будет искать по всем городам)
2) Проверяет есть ли в кеше объявления, соответствующие данному запросу. Если есть, проверяет статус объявления. Если объявление закрыто, выставляет новый статус и обновляет поле update_time
После проверяет изменения в полях price, name и descriptions. Если они есть, то обновляет данные поля и поле update_time. Все изменения вносятся в таблицу кеша в БД SQLite
3) Далее программа находит ссылки на объявления, соответствующие нашему запросу на первых pages_count страницах вывода. 
4) После программа проходит по первым ads_count найденным ссылкам и собирает данные: ID объявления, название, цену, адрес, описание, дату публикации(по московскому времени), кол-во просмотров, url, статус объявления.
Все эти данные, а также сам поисковый запрос и время исполнения программы добавляются в таблицу кеша БД.
#Сейчас у pages_count и ads_count выставлены небольшие значения из-за частого вылета по 429 статусу. Должен помочь набор proxy-серверов.
5) Все данные из БД, которые соответствуют запросу сохраняются в файл result.txt в корневой директории.

TO_DO:
1) Реализовать класс управления БД
2) Найти proxy для тестирования при высоких нагрузках
3) Переписать метод parse_ads_page для работы со списком url'ов снаружи(разобраться с driver и методом __set_up внутри класса)
4) Добавить считывание телефона(Нужна регистрация?)
5) Добавить сохранение изображений из объявления. (BLOB в SQLite?)
