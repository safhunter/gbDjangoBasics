from django.db import models
from django.conf import settings

from geekshop.common import GetItemMixin
from mainapp.models import Product


class Basket(GetItemMixin, models.Model):
    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket',
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0,
    )

    add_datetime = models.DateTimeField(
        verbose_name='добавлен',
        auto_now_add=True,
    )

    # @staticmethod
    # def get_item(pk):
    #     return Basket.objects.filter(pk=pk).first()
    #
    # @staticmethod
    # def get_items(user):
    #     return Basket.objects.filter(user=user)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = Basket.objects.filter(user=self.user)
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost

    is_active = models.BooleanField(
        verbose_name='активна',
        default=True,
    )

    def __str__(self):
        return f'{self.product.name}({self.user.username})'
