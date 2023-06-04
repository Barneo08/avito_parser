import os
import sqlite3 as sq
import pandas as pd
from src.avito_parser import AvitoParser
from datetime import datetime, timedelta
from src.helpers import transliterate


if __name__ == '__main__':

    current_time = (datetime.now() - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M')
    request = input('Введите поисковый запрос: ').lower()
    city = input('Введите город поиска: ').lower()

    if not city:
        city = 'all'

    avitoparser = AvitoParser(
        request=request.lower(),
        city=city
    )

    db = sq.connect(os.path.join("src", "query_cache.db"))
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS query_cache(    
        ad_id BIGINT NOT NULL PRIMARY KEY,
        date_public DATETIME,
        views INT,
        price TEXT,
        name TEXT,
        address TEXT,
        descriptions TEXT,
        url TEXT,
        city TEXT,
        request TEXT,
        is_closed INT,
        add_time DATETIME,
        update_time DATETIME
    )""")
    db.commit()

    viewed_list = []
    db.row_factory = sq.Row
    if city == 'all':
        res = db.execute("SELECT * FROM query_cache WHERE request = ?", (request,)).fetchall()
        query = f"SELECT * FROM query_cache WHERE request = '{request}'"
    else:
        res = db.execute("SELECT * FROM query_cache WHERE request = ? AND city = ?",
                         (request, transliterate(city))).fetchall()
        query = f"SELECT * FROM query_cache WHERE request = '{request}' AND city = '{transliterate(city)}'"
    if res:
        for item in res:
            viewed_list.append({k: item[k] for k in item.keys()})

        for item in viewed_list:
            current_cache_page = avitoparser.parse_ads_page(item['url'])
            if current_cache_page['is_closed']:
                db.execute("UPDATE query_cache SET is_closed = ?, update_time = ? WHERE ad_id = ?",
                           (1, current_time, item['ad_id']))
                continue
            if item['price'] != current_cache_page['price']:
                db.execute("UPDATE query_cache SET price = ?, update_time = ? WHERE ad_id = ?",
                           (current_cache_page['price'], current_time, item['ad_id']))
            if item['name'] != current_cache_page['name']:
                db.execute("UPDATE query_cache SET name = ?, update_time = ? WHERE ad_id = ?",
                           (current_cache_page['name'], current_time, item['ad_id']))
            if item['descriptions'] != current_cache_page['descriptions']:
                db.execute("UPDATE query_cache SET descriptions = ?, update_time = ? WHERE ad_id = ?",
                           (current_cache_page['descriptions'], current_time, item['ad_id']))

    my_list = avitoparser.parse_pages_from_url_list()
    for elem in my_list:
        if elem['ad_id'] not in [item['ad_id'] for item in viewed_list]:
            elem['request'] = request
            elem['add_time'] = current_time
            elem['update_time'] = current_time
            db.execute(
                """INSERT INTO query_cache (
                    ad_id,
                    name,
                    price,
                    address,
                    descriptions,
                    date_public,
                    views,
                    is_closed,
                    url,
                    city,
                    request,
                    add_time,
                    update_time
                )
                VALUES (
                    :ad_id,
                    :name,
                    :price,
                    :address,
                    :descriptions,
                    :date_public,
                    :views,
                    :is_closed,
                    :url,
                    :city,
                    :request,
                    :add_time,
                    :update_time
                )""",
                elem,
            )
        else:
            print('skip ', elem['ad_id'])
    db.commit()

    df = pd.read_sql(query, db)
    try:
        df.to_excel(os.path.join('result.xlsx'))
    except PermissionError:
        print('Необходимо закрыть файл result.txt')
    finally:
        db.close()