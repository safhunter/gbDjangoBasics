from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.utils.timezone import now

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from geekshop.views import get_menu_context


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST or None)

    next = request.GET['next'] if 'next' in request.GET.keys() else '/'
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth.login(request, user)
                # if 'next' in request.POST.keys():
                #     return HttpResponseRedirect(request.POST['next'])
                return HttpResponseRedirect(request.POST['next'])
                # return HttpResponseRedirect(reverse('main'))
            else:
                messages.warning(request, 'Пользователь не активирован. Ссылка для активации отправлена на ваш Email')
                send_verify_email(user)

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

    context = {
        'title': title,
        'menu_list': get_menu_context(),
    }

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            if ShopUser.objects.filter(email=register_form.fields['email']).count() > 0:
                messages.warning(request, 'Данный email уже зарегистрирован')
                register_form.fields['email'] = ''
                context['register_form'] = register_form
                return render(request, 'authapp/register.html', context)
            user = register_form.save()
            if send_verify_email(user):
                messages.success(request, 'Ссылка для активации отправлена на ваш Email')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                messages.error(request, 'Извините, в данный момент отправка Email не доступна. Попробуйте попозже.')
                register_form.fields['email'] = ''
                context['register_form'] = register_form
                return render(request, 'authapp/register.html', context)
    else:
        register_form = ShopUserRegisterForm()

    context['register_form'] = register_form

    return render(request, 'authapp/register.html', context)


def edit(request):
    title = 'редактирование'

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
        'menu_list': get_menu_context(),
    }

    return render(request, 'authapp/edit.html', context)


def verify(request, activation_key):
    context = {
        'is_activation_ok': False,
    }
    try:
        user = ShopUser.objects.get(activation_key=activation_key)
        if not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key_expires = now()
            user.save()
            auth.login(request, user)
            context['is_activation_ok'] = True
            return render(request, 'authapp/verify.html', context)
        else:
            messages.error(request, 'Истек срок действия ключа активации')
            return render(request, 'authapp/verify.html', context)
    except ObjectDoesNotExist as ex:
        print(f'Error activation user: {ex.args}')
        messages.error(request, 'Ошибка активации пользователя')
        return render(request, 'authapp/verify.html', context)
        # return HttpResponseRedirect(reverse('main'))


def send_verify_email(user):
    user.generate_new_activation_key()
    user.save()
    verify_link = reverse('auth:verify', args=[user.activation_key])

    title = f'Подтвердите учетную запись {user.username}'

    message = f'Для подтверждения учетной записи {user.username}' \
            f'на портале {settings.DOMAIN_NAME} перейдите по ссылке: \n' \
            f'{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

