from django.db import models
from product.models import Product
from supplier.models import Supplier


class Supply(models.Model):
    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplies', verbose_name='Поставщик')
    delivery_date = models.DateField(verbose_name='Дата поставки')

    def __str__(self):
        return f'Поставщик: {self.supplier}({self.delivery_date})'


class SupplyProduct(models.Model):
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, related_name='supply_products', verbose_name='Поставщик')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='supply_products', verbose_name='Товар')
    quantity = models.IntegerField(verbose_name='Количество товара')