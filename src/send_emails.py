import os
import sys
import django
import datetime
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives


project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)  # запуск django вне проекта
os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'


django.setup()
from scraping.models import Vacancy, Error, Url, City, Language
from src.settings import EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()
#today = timezone.date()
subject = f'Job posting on {today}'
text_content = f'New vacancies for you'
from_email = EMAIL_HOST_USER
empty = '<h2>Sorry, but nowadays there is no vacancies for you.</h2>'

User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dict = {}
for i in qs:
    users_dict.setdefault((i['city'], i['language']), [])
    users_dict[(i['city'], i['language'])].append(i['email'])  # список мейлов с двойным ключом
if users_dict:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])

    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)
    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h4><a href="{row["url"]}">{ row["title"] }</a></h4>'
            html += f'<p>{ row["description"] }</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            #msg.send()

qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
_html = ''
to = ADMIN_USER

if qs.exists():  #отправка ошибок скрапинга
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        _html += f'<p><a href="{i["url"]}">{ i["title"] }</a></p><br>'
    subject = f'Scraping errors {today}'
    text_content = f'Scraping errors'
    data = error.data.get('user_data')
    if data:
        _html += '<hr>'
        _html += '<h2>Users wishes </h2>'
        for i in data:
            _html += f'<p>City: {i["city"]}, Language: {i["language"]}, Email: {i["email"]}</p><br>'
        subject = f'Users wishes {today}'
        text_content = f'Users wishes'

qs = Url.objects.all().values('city', 'language')
urls_dict = {(i['city'], i['language']): True for i in qs}
urls_err = ''
for keys in users_dict.keys():  #отправка ошибок из-за отсутствия урлов
    if keys not in urls_dict:
        if keys[0] and keys[1]:
            city = City.objects.get(pk=keys[0])
            language = Language.objects.get(pk=keys[1])
            urls_err += f'<p> There is not urls for city {city} and language {language}</p><br>'
if urls_err:
    subject += ' Missing urls'
    _html += urls_err

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()