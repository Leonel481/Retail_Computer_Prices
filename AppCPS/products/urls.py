from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('product/<str:codes>', get_product, name='get_product'),
]