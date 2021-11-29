from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.db import DatabaseError

from basketapp.models import Basket
from ordersapp.models import OrderItem


@receiver(pre_save, sender=OrderItem, dispatch_uid='order_item_put_products_into_order')
@receiver(pre_save, sender=Basket, dispatch_uid='basket_put_products_into_basket')
def get_products_from_warehouse(sender, instance, **kwargs):
    try:
        if instance.pk:
            products_to_get = instance.quantity - sender.get_item(pk=instance.pk).quantity
        else:
            products_to_get = instance.quantity
        if products_to_get != 0:
            instance.product.quantity -= products_to_get
            instance.product.save()
    except DatabaseError as err:
        print(f'Can\'t get product from warehouse:\n {err}')
        raise err


@receiver(pre_delete, sender=OrderItem, dispatch_uid='order_item_return_products_into_warehouse')
@receiver(pre_delete, sender=Basket, dispatch_uid='basket_return_products_into_warehouse')
def return_products_into_warehouse(sender, instance, **kwargs):
    try:
        instance.product.quantity += instance.quantity
        instance.product.save()
    except DatabaseError as err:
        print(f'Can\'t return product into warehouse:\n {err}')
        raise err
