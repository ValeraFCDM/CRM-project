from django.db import models
from company.models import Company


class Storage(models.Model):
    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    address = models.CharField(max_length=255, blank=False, verbose_name='Адрес')
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='storage')

    def __str__(self):
        return f'Склад: {self.address}'
