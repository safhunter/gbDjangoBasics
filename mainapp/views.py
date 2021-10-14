from django.shortcuts import render
from geekshop.views import get_menu_context, add_list_marks
import json
import os
import io
from pathlib import Path

from mainapp.models import ProductCategory


def products(request):
    title = 'Каталог'

    links_menu = ProductCategory.objects.all()
    # links_menu = []
    # try:
    #     with io.open(os.path.join(Path(__file__).resolve().parent, 'templates', 'mainapp', 'product_menu.json'),
    #                  'r', encoding='utf-8-sig') as json_file:
    #         links_menu = json.load(json_file)
    # except Exception as ex:
    #     print(ex)
    #     pass    # todo: add exception handler
    # links_menu = add_list_marks(links_menu)

    context = {
        'title': title,
        'links_menu': links_menu,
        'menu_list': get_menu_context(),
    }

    return render(request, 'mainapp/products.html', context)
