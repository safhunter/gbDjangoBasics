from django.shortcuts import render, get_object_or_404
from geekshop.views import get_menu_context


from mainapp.models import ProductCategory, Product


def products(request, pk=None):
    title = 'Каталог'

    links_menu = ProductCategory.objects.all().order_by('name')
    products = Product.objects.all().order_by('price')

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
        }

        return render(request, 'mainapp/products.html', context)

    same_products = Product.objects.all()[1:2]
    context = {
        'title': title,
        'links_menu': links_menu,
        'menu_list': get_menu_context(),
        'same_products': same_products,
        'products': products,
    }

    return render(request, 'mainapp/products.html', context)
