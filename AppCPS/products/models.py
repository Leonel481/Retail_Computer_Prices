from django.db import models
from django.utils import timezone

# Create your models here.
class product(models.Model):
    id = models.AutoField(primary_key=True)
    titles = models.CharField(max_length = 200)
    links = models.URLField(null=True)
    codes = models.CharField(max_length= 10)
    stocks = models.IntegerField(null=True)
    ratings = models.PositiveIntegerField(null=True)
    prices_usd = models.DecimalField(decimal_places= 2, max_digits=10)
    prices_pen = models.DecimalField(decimal_places= 2, max_digits=10)
    images = models.URLField(null=True)
    Fecha = models.DateTimeField(null=True, blank=True)
    categoria = models.ForeignKey(
            'products.Category', on_delete=models.CASCADE, related_name='products')
    empresa = models.ForeignKey(
            'products.Company', on_delete=models.CASCADE, related_name='products')
    marca = models.ForeignKey(
            'products.Brand', on_delete=models.CASCADE, related_name='products')
    def __str__(self):
        return f'{self.titles} | {self.categoria} | {self.marca} | {self.empresa}'

class Brand(models.Model):
    marca = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now
    )
    def __str__(self) -> str:
        return self.marca

class Category(models.Model):
    categoria = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now
    )
    def __str__(self) -> str:
        return self.categoria

class Company(models.Model):
    empresa = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now
    )
    def __str__(self) -> str:
        return self.empresa