import phonenumbers
from django import template

register = template.Library()


# @register.filter(name='phonenumber')
# def phonenumber(value, country=None):
#     return phonenumbers.parse(value, country)
