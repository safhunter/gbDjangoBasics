from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Product


@receiver(post_save, sender=Product, dispatch_uid='product_post_save_signal')
def product_post_save_handler(sender, instance, created, **kwargs):
    if created:
        print(f'Add new product in category {instance.category}')  # todo: remove debug string
        instance.category.add_product()


@receiver(post_delete, sender=Product, dispatch_uid='product_delete_signal')
def product_delete_handler(sender, instance, **kwargs):
    print(f'Remove product from category {instance.category}')  # todo: remove debug string
    instance.category.remove_product()


@receiver(pre_save, sender=Product, dispatch_uid='product_pre_save_signal')
def product_pre_save_handler(sender, instance, **kwargs):
    product = Product.objects.filter(pk=instance.pk).first()
    if product:
        if product.category.pk != instance.category.pk:
            product.category.remove_product()
            instance.category.add_product()
            # todo: remove debug string
            print(f'Move product from category {product.category} to category {instance.category}')
