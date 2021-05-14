import os
import sys

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)                                             #запуск django вне проекта
os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'

import django
django.setup()

from django.db import DatabaseError

from scraping.parsers import *
from scraping.models import City, Language, Vacancy

parsers = (
           (rabota_by, 'https://rabota.by/search/vacancy?clusters=true&area=1002&no_magic=true&enable_snippets=true&salary=&st=searchVacancy&text=Python'),
           (dev_by, 'https://jobs.dev.by/?&filter[search]=python%20')
           )
city = City.objects.filter(slug='minsk').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()