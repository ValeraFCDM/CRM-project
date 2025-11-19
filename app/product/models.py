from django.db import models
from storage.models import Storage

class Product(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    title = models.CharField(max_length=100, unique=True, verbose_name='Наименование товара')
    description = models.CharField(max_length=255, verbose_name='Описание')
    purchase_price = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Закупочная цена')
    sale_price = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Розничная цена')
    quantity = models.IntegerField(default=0, verbose_name='Количество на складе')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='products', verbose_name='Склад')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    def __str__(self):
        return f'Товар: {self.title} (ID {self.id})'