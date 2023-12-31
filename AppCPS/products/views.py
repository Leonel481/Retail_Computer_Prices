from django.shortcuts import render, redirect
from django.db.models import Max, Prefetch
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required # permissions_required
import pandas as pd
import plotly.express as px
from .models import *
from .forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def index(request):

    #Obtener la fecha más reciente para cada 'codes'
    max_dates = Product.objects.values('codes').annotate(max_date=Max('Fecha'))
    #Convertir max_dates de diccionarios a una lista de tuplas
    max_dates = list(max_dates.values_list('codes', 'max_date'))
    
    #Crear consulta para filtrar en la BD
    q_objects = Q()
    for codes, Fecha in max_dates:
        q_objects |= Q(codes=codes, Fecha=Fecha)

    products = Product.objects.filter(q_objects).order_by('titles') 

    products = Product.objects.filter(q_objects)

    # Buscador por categoria
    if 'categoria' in request.GET:
        categoria_id = request.GET['categoria']
        if categoria_id == '':
            products_f = products
        else:
            products_f = products.filter(categoria=categoria_id)
    else:
        products_f = products

    categories = Category.objects.all()

    # Número de elementos por página
    elementos_por_pagina = 32  # Puedes ajustar este número según tus necesidades

    paginator = Paginator(products_f, elementos_por_pagina)
    pagina = request.GET.get('pagina')

    try:
        elementos_paginados = paginator.page(pagina)
    except PageNotAnInteger:
        # Si la página no es un número, muestra la primera página
        elementos_paginados = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, muestra la última página
        elementos_paginados = paginator.page(paginator.num_pages)
                                    
    return render(request, 'products/list_of_products.html', {'elementos': elementos_paginados,
                                                              'categories': categories})



def get_product(request, id):
    #Obtener el producto
    product = Product.objects.filter(codes=id).order_by('-Fecha').first()


    # graficar el historico de precios del producto
    products_graph = Product.objects.filter(codes=id).order_by('-Fecha')
    dates = [product.Fecha for product in products_graph]
    prices_usd = [product.prices_usd for product in products_graph]
    fig = px.line(x=dates, y=prices_usd, title='Evolución del precio del producto en el tiempo')

    fig.update_xaxes(title_text='Fecha')
    fig.update_yaxes(title_text='Precio USD')

    #Convertir en grafico html
    html_graph = fig.to_html(full_html=False, include_plotlyjs='cdn')

    comments = Comment.objects.filter(product=id)
    form = CommentForm()
    return render(request, 'products/show_product.html',
    {'product':product, 'html_graph': html_graph,
    'comments': comments, 'form': form})

@login_required
def add_new_comment(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            product = Codes.objects.get(id=id)

            new_comment = form.save(commit=False)
            new_comment.author = user
            new_comment.product = product

            new_comment.save()
    
    return redirect('get_product', id)

    # else:
    #     return redirect('get_product', id)


def buscar_producto(request):
    
    q = request.GET.get('q', '')
    productos_buscados = Product.objects.filter(Q(titles__icontains=q))
    return render(request, 'products/busqueda.html', {'productos_buscados': productos_buscados})