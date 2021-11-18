from geekshop.views import get_menu_context


def menu(request):
    print(f'context processor menu works')

    return {
       'menu_list': get_menu_context(request),
    }
