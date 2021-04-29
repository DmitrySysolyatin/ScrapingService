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
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name