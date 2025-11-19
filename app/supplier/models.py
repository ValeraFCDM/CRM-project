from django.db import models
from company.models import Company

class Supplier(models.Model):
    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='suppliers', verbose_name='Компания')
    title = models.CharField(max_length=100, verbose_name='Название')
    inn = models.CharField(max_length=12, unique=True, verbose_name='ИНН')

    def __str__(self):
        return f'{self.title}({self.inn})'