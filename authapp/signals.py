from django.db.models.signals import post_save
from django.dispatch import receiver

from authapp.models import ShopUser, ShopUserProfile


@receiver(post_save, sender=ShopUser, dispatch_uid='user_post_save_signal')
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        ShopUserProfile.objects.create(user=instance)
    else:
        instance.shopuserprofile.save()
