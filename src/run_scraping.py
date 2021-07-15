import asyncio
import os
import sys
import datetime as dt
from django.contrib.auth import get_user_model

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)  # запуск django вне проекта
os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'

import django

django.setup()

from django.db import DatabaseError

from scraping.parsers import *
from scraping.models import Vacancy, Error, Url

User = get_user_model()

parsers = (
    (rabota_by, 'rabota_by'),
    (dev_by, 'dev_by')
)

jobs, errors = [], []

def get_settings():
    qs = Url.objects.filter().values()
    settings_set = set((q['city_id'], q['language_id']) for q in qs)  # генератор делает сет кортежей из id города и языка
    return settings_set


def get_urls(_settings):
    qs = Url.objects.all().values()  # все данные из БД
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:  # полученные данные
        if pair in url_dict:
            tmp = {'city': pair[0], 'language': pair[1], 'url_data': url_dict[pair]}
            urls.append(tmp)
    return urls

  # асинхронный запуск

async def main(value):
    func, url, city, language = value
    job, error = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(error)
    jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)

loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             # набор функций и данных(урлы, города и языки) для асинхронного запуска
             for data in url_list  # функции для выполнения
             for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])  # запуск на выполнение
loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    v = Vacancy(**job)  # раскрытие словаря
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        er = qs.first()
        er.data.update({'errors': errors})
        er.save()
    else:
        er = Error(data=f'errors:{errors}').save()

ten_days_ago = dt.date.today() - dt.timedelta(10)
Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()
