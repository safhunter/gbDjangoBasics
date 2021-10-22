from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

from basketapp.models import Basket
from geekshop.views import get_menu_context
from mainapp.models import Product


def basket(request):
    title = 'Корзина'

    basket = Basket.objects.filter(user=request.user)

    context = {
        'title': title,
        'menu_list': get_menu_context(),
        'basket': basket,
    }
    return render(request, 'basketapp/basket.html', context)


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request):
    context = {
        'menu_list': get_menu_context(),
    }
    return render(request, 'basketapp/basket.html', context)
