from django.core.management.base import BaseCommand
import os
import json

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product, OfficeContact
from django.core.exceptions import ObjectDoesNotExist


JSON_PATH = 'mainapp/jsons'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            try:
                _category = ProductCategory.objects.get(name=category_name)
            except ObjectDoesNotExist as ex:
                print(f'Trying to add a product of unknown category (Product moved to category "Прочее"), cause: {ex}')
                _category = ProductCategory.objects.get_or_create(name='Прочее')[0]
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        office_contacts = load_from_json('officecontacts')

        OfficeContact.objects.all().delete()
        for contact in office_contacts:
            new_contact = OfficeContact(**contact)
            new_contact.save()

        super_user = ShopUser.objects.create_superuser('admin', 'admin@geekshop.local', '123', age=36)
        super_user.save()

        if super_user:
            print('Super user created.')
