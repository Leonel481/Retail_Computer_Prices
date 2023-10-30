from django.db import models

# Create your models here.
class product(models.Model):
    titles = models.CharField(max_length = 200)
    links = models.URLField(null=True)
    codes = models.CharField(max_length= 10)
    stocks = models.IntegerField(null=True)
    ratings = models.PositiveIntegerField(null=True)
    prices_usd = models.DecimalField(decimal_places= 2, max_digits=10)
    prices_pen = models.DecimalField(decimal_places= 2, max_digits=10)
    images = models.URLField(null=True)
    Fecha = models.DateTimeField(null=True, blank=True)
    categoria = models.CharField(max_length= 50)
    empresa = models.CharField(max_length= 50)
    marca = models.CharField(max_length= 50)
