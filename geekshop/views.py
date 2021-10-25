from django.shortcuts import render
import json
import os
import io
from pathlib import Path

from basketapp.models import Basket
from mainapp.models import Product, OfficeContact


#  Adds a 'mark' field to each item in the list.
def add_list_marks(source_list: list):
    for item in source_list:
        try:
            url_path = item['href']
            if url_path[0] == '\\' or url_path[0] == '/':
                url_path = url_path[1:]     # todo: add relative link marks
            if url_path == '':
                item['mark'] = url_path
                continue
            if url_path[-1] != '/' and url_path[-1] != '\\':
                url_path = url_path + '/'
            else:
                url_path[-1] = '/'
            item['mark'] = url_path
        except TypeError:
            continue
        except KeyError:
            item['mark'] = ''
    return source_list


def get_menu_context():
    menu_list = []
    try:
        with io.open(os.path.join(Path(__file__).resolve().parent, 'templates', 'geekshop', 'menu_list.json'),
                     'r', encoding='utf-8-sig') as json_file:
            menu_list = json.load(json_file)
    except Exception as ex:
        print(ex)
        pass  # todo: add exception handler

    return add_list_marks(menu_list)


def main(request):
    title = 'Магазин'
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    products = Product.objects.all()[:4]

    context = {
        'title': title,
        'menu_list': get_menu_context(),
        'products': products,
        'basket': basket,
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    title = 'Контакты'

    location = OfficeContact.objects.all()[0]
    context = {
        'title': title,
        'menu_list': get_menu_context(),
        'location': location,
    }
    return render(request, 'geekshop/contact.html', context)
