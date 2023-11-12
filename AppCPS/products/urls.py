from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('product/<int:id>', get_product, name='get_product'),
    path('buscar/', buscar_producto, name='buscar_producto'),
    path('product/<int:id>/add_new_comment', add_new_comment, name='add_new_comment')
]