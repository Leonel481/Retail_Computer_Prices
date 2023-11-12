from django.db import models
from django.utils import timezone

# Create your models here.
class Codes(models.Model):
    codes = models.CharField(max_length= 30, unique=True)
    # Fecha_max = models.DateTimeField(null=True, blank=True) 
    # created_date = models.DateTimeField(
    #     default=timezone.now
    # )
    def __str__(self) -> str:
        return self.codes


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    titles = models.CharField(max_length = 200)
    links = models.URLField(null=True)
    codes = models.ForeignKey(
            'products.Codes', on_delete=models.CASCADE, related_name='products')
    stocks = models.IntegerField(null=True)
    ratings = models.PositiveIntegerField(null=True, blank=True) 
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
    marca = models.CharField(max_length=50, unique=True)
    # created_date = models.DateTimeField(
    #     default=timezone.now
    # )
    def __str__(self) -> str:
        return self.marca

class Category(models.Model):
    categoria = models.CharField(max_length=50, unique=True)
    # created_date = models.DateTimeField(
    #     default=timezone.now
    # )
    def __str__(self) -> str:
        return self.categoria

class Company(models.Model):
    empresa = models.CharField(max_length=50, unique=True)
    # created_date = models.DateTimeField(
    #     default=timezone.now
    # )
    def __str__(self) -> str:
        return self.empresa
    
class Comment(models.Model):
    product = models.ForeignKey(
        'products.Codes', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=255)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self) -> str:
        return self.text