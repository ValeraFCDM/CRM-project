from django.db import models

class Company(models.Model):
    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    inn = models.CharField(max_length=12, unique=True, blank=False, verbose_name='ИНН')
    title = models.CharField(max_length=100, blank=False, verbose_name='Название')

    def __str__(self):
        return f'{self.title}({self.inn})'