from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ProductCategory(models.Model):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

    name = models.CharField(
        max_length=64,
        verbose_name='имя',
        unique=True,
    )

    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        auto_now=True,
    )
    #
    # _products_count = models.PositiveIntegerField(
    #     verbose_name='количество товаров',
    #     default=0,
    # )
    #
    # def add_product(self):
    #     self._products_count += 1
    #     self.save()
    #
    # def remove_product(self):
    #     if self._products_count > 0:
    #         self._products_count -= 1
    #         self.save()

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        verbose_name='категория',
    )

    name = models.CharField(
        max_length=128,
        verbose_name='имя продукта',
    )

    image = models.ImageField(
        upload_to='product_images',
        blank=True,
    )

    short_desc = models.CharField(
        max_length=64,
        verbose_name='краткое описание',
    )

    description = models.TextField(
        verbose_name='описание продукта',
        blank=True,
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='цена',
    )

    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0,
    )

    def __str__(self):
        return f'{self.name} ({self.category.name})'


class OfficeContact(models.Model):
    class Meta:
        verbose_name = 'контакты офиса'
        verbose_name_plural = 'контакты офисов'

    city = models.CharField(
        max_length=128,
        verbose_name='город',
    )

    phone_number = PhoneNumberField(
        blank=True,
        verbose_name='номер телефона',
    )

    email = models.EmailField(
        verbose_name='E-mail',
        blank=True,
    )

    address = models.CharField(
        max_length=255,
        verbose_name='адрес',
        blank=True,
    )

    def __str__(self):
        return f'{self.city}, {self.address}'
