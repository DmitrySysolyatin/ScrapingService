from django.db import models

class City(models.Model):
    name = models.CharField(max_length=20, unique=True)
                            #verbose_name = 'Город'
    slug = models.CharField(max_length=20, blank=True, unique=True)

    class Meta:
        #verbose_name = 'Город'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, blank=True, unique=True)

    class Meta:
        # verbose_name = 'Город'
        verbose_name_plural = 'Programming languages'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name ='Title')
    company = models.CharField(max_length=250, verbose_name='Company')
    description = models.TextField(verbose_name='Vacation description')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='City')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Programming language')
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Vacancies'

    def __str__(self):
        return self.title