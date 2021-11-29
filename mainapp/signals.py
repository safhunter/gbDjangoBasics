from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Product


@receiver(post_save, sender=Product, dispatch_uid='product_add_product_to_category')
def add_product_to_category(sender, instance, created, **kwargs):
    if created:
        print(f'Add new product in category {instance.category}')  # todo: remove debug string
        instance.category.add_product()


@receiver(post_delete, sender=Product, dispatch_uid='product_delete_product_from_category')
def delete_product_from_category(sender, instance, **kwargs):
    print(f'Remove product from category {instance.category}')  # todo: remove debug string
    instance.category.remove_product()


@receiver(pre_save, sender=Product, dispatch_uid='product_change_product_category')
def change_product_category(sender, instance, **kwargs):
    product = Product.objects.filter(pk=instance.pk).first()
    if product:
        if product.category.pk != instance.category.pk:
            product.category.remove_product()
            instance.category.add_product()
            # todo: remove debug string
            print(f'Move product from category {product.category} to category {instance.category}')


@receiver(pre_save, sender=Product, dispatch_uid='product_change_product_activity')
def change_product_activity(sender, instance, **kwargs):
    if instance.quantity < 1:
        instance.is_active = False
