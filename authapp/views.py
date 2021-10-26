from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from basketapp.models import Basket
from geekshop.views import get_menu_context


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST or None)

    next = request.GET['next'] if 'next' in request.GET.keys() else '/'
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            # if 'next' in request.POST.keys():
            #     return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(request.POST['next'])
            # return HttpResponseRedirect(reverse('main'))

    context = {
        'title': title,
        'login_form': login_form,
        'menu_list': get_menu_context(),
        'next': next,
    }

    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'register_form': register_form,
        'menu_list': get_menu_context(),
    }

    return render(request, 'authapp/register.html', context)


def edit(request):
    title = 'редактирование'

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserRegisterForm(instance=request.user)

    context = {
        'title': title,
        'edit_form': edit_form,
        'basket': basket,
        'menu_list': get_menu_context(),
    }

    return render(request, 'authapp/edit.html', context)
