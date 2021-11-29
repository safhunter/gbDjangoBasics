from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
import hashlib
import random


class ShopUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='users_avatars',
        blank=True,
    )

    age = models.PositiveIntegerField(
        verbose_name='возраст',
        default=18,
    )

    activation_key = models.CharField(
        max_length=128,
        blank=True,
    )

    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48)),
    )

    def is_activation_key_expired(self):
        if now() < self.activation_key_expires:
            return False
        return True

    def generate_new_activation_key(self):
        self.activation_key_expires = now() + timedelta(hours=48)
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        self.activation_key = hashlib.sha1((self.email + salt).encode('utf8')).hexdigest()
        return self.activation_key


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(
        ShopUser,
        unique=True,
        null=False,
        db_index=True,
        on_delete=models.CASCADE
    )

    tagline = models.CharField(verbose_name='тэги', max_length=128, blank=True)

    about_me = models.TextField(verbose_name='о себе', max_length=512, blank=True)

    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)
