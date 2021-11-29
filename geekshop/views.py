from django.shortcuts import render
import json
import os
import io
from pathlib import Path

from mainapp.models import Product, OfficeContact


#  Adds a 'mark' field to each item in the list.
def add_list_marks(source_list: list, request):
    path = request.path.replace('/', '')
    for num, item in enumerate(source_list):
        try:
            item['active'] = False
            if item['href'][0] == '/':  # root link
                item_path = item['href'].replace('/', '')
                if item_path:
                    if path.startswith(item_path):
                        item['active'] = True
                elif item_path == path:
                    item['active'] = True
            else:   # relative link
                item_path = item['href'].replace('/', '')
                if item_path in path:
                    item['active'] = True
        except (TypeError, KeyError):
            source_list[num] = {
                'href': '/',
                'name': '',
                'active': False,
            }
    return source_list


def get_menu_context(request):
    menu_list = []
    try:
        with io.open(os.path.join(Path(__file__).resolve().parent, 'templates', 'geekshop', 'menu_list.json'),
                     'r', encoding='utf-8-sig') as json_file:
            menu_list = json.load(json_file)
    except Exception as ex:
        print(ex)
        pass  # todo: add exception handler

    return add_list_marks(menu_list, request)


def main(request):
    title = 'Магазин'

    products = Product.objects.all()[:4]

    context = {
        'title': title,
        'products': products,
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    title = 'Контакты'

    location = OfficeContact.objects.all()[0]
    context = {
        'title': title,
        'location': location,
    }
    return render(request, 'geekshop/contact.html', context)
