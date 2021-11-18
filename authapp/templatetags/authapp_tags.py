from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_link_users')
def media_link_users(media):
    if not media:
        media = 'users_avatars/default.jpg'
    elif str(media).startswith('https://') or str(media).startswith('http://'):
        return f'{media}'

    return f'{settings.MEDIA_URL}{media}'
