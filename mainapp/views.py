from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from geekshop.views import get_menu_context
from mainapp.models import ProductCategory, Product
import random


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)
    return same_products


def products(request, pk=None):
    title = 'Каталог'

    links_menu = ProductCategory.objects.all().order_by('name')
    products = Product.objects.all().order_by('price')
    basket = get_basket(request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            'title': title,
            'links_menu': links_menu,
            'menu_list': get_menu_context(),
            'category': category,
            'products': products,
            'basket': basket,
        }

        return render(request, 'mainapp/products.html', context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'title': title,
        'links_menu': links_menu,
        'menu_list': get_menu_context(),
        'same_products': same_products,
        'products': products,
        'basket': basket,
        'hot_product': hot_product,
    }

    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    title = 'Товар'
    links_menu = ProductCategory.objects.all().order_by('name')
    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': title,
        'links_menu': links_menu,
        'menu_list': get_menu_context(),
        'same_products': get_same_products(product),
        'product': product,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/product.html', context)
