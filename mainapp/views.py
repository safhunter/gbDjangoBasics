from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from mainapp.models import ProductCategory, Product
import random


def get_hot_product(selected_products):
    return random.sample(list(selected_products), 1)[0]


def get_same_products(all_products, selected_product):
    same_products = all_products.filter(category=selected_product.category).exclude(pk=selected_product.pk)
    return same_products


def products(request, pk=None, page=1):
    title = 'Каталог'

    links_menu = ProductCategory.objects.all().order_by('name')
    all_products = Product.objects.filter(is_active=True,
                                          category__is_active=True,
                                          quantity__gte=1).select_related('category').order_by('price')

    if pk is not None:
        if pk == 0:
            category = {'pk': 0, 'name': 'все'}
            result_products = all_products
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            result_products = all_products.filter(category__pk=pk).order_by('price')

        paginator = Paginator(result_products, 2)

        try:
            products_paginator = paginator.page(page)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }

        return render(request, 'mainapp/products.html', context)

    hot_product = get_hot_product(all_products)
    same_products = get_same_products(all_products, hot_product)
    result_products = all_products

    context = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'products': result_products,
        'hot_product': hot_product,
    }

    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    title = 'Товар'
    links_menu = ProductCategory.objects.all().order_by('name')
    selected_product = get_object_or_404(Product, pk=pk)
    all_products = Product.objects.filter(is_active=True,
                                          category=selected_product.category,
                                          quantity__gte=1).select_related('category')

    context = {
        'title': title,
        'links_menu': links_menu,
        'same_products': get_same_products(all_products, selected_product),
        'product': selected_product,
    }
    return render(request, 'mainapp/product.html', context)
