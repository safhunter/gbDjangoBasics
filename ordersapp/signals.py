from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from django.db import transaction, DatabaseError

from mainapp.models import Product
from ordersapp.models import Order, OrderItem


@receiver(pre_save, sender=Order, dispatch_uid='order_put_products_into_order')
def put_products_into_order(sender, instance, **kwargs):
    old_order = sender.objects.filter(pk=instance.pk)
    if old_order and not old_order.is_active and instance.is_active:
        try:
            with transaction.atomic():
                for item in instance.orderitems.select_related():
                    item.product.quantity -= item.quantity
                    item.product.save()
        except DatabaseError as err:
            instance.is_active = False
            print(f'Can\'t get products from warehouse:\n {err}' )


@receiver(pre_delete, sender=Order, dispatch_uid='order_return_products_into_warehouse')
def return_products_into_warehouse(sender, instance, **kwargs):
    for item in instance.orderitems.select_related():
        item.product.quantity += item.quantity
        item.product.save()


@receiver(pre_save, sender=OrderItem, dispatch_uid='order_item_update_fixed_price')
def update_fixed_price(sender, instance, **kwargs):
    instance.set_product_fixed_price(instance.product.price)


@receiver(post_save, sender=Product, dispatch_uid='product_update_fixed_price')
def update_fixed_price(sender, instance, created, **kwargs):
    if not created:
        for order_item in OrderItem.objects.filter(product__pk=instance.pk):
            order_item.save()
