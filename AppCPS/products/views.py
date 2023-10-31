from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    #business logical
    products = product.objects.all()
    return render(request, 'products/list_of_products.html', {'products':products})

def get_product(request):
    product = product.objects.get(id=id)
    return render(request, 'products/show_product.html', {'product':product})