from django.db import models
from django.utils.timezone import now

from employee.models import Employee


class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    description = models.CharField(max_length=100)
    weight = models.DecimalField(
        max_digits=7,
        decimal_places=3,
        null=True)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=13, decimal_places=3)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='products'
    )

    def __str__(self):
        return self.description


class Sale(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='sales'
    )
    products = models.ManyToManyField(
        Product,
        through='ProductsSales',
    )
    datetime = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.employee.surname) + str(self.datetime)


class ProductsSales(models.Model):
    price = models.DecimalField(max_digits=13, decimal_places=3)
    sale = models.ForeignKey(
        Sale,
        on_delete=models.PROTECT,
        related_name='products_sales')
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='products_sales')
