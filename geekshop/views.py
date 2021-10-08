from django.shortcuts import render


def main(request):
    return render(request, 'geekshop/index.html')


def contacts(request):
    return render(request, 'geekshop/contact.html')
