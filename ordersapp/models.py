from django.conf import settings
from django.db import models

from geekshop.common import GetItemMixin
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'
    FINISHED = 'FSD'

    ORDER_PAID_STATUSES = (
        PAID,
        READY,
        FINISHED,
    )

    ORDER_STATUS = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (FINISHED, 'завершен'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        verbose_name='создан',
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name='изменен',
        auto_now=True,
    )
    status = models.CharField(
        verbose_name='статус',
        max_length=3,
        choices=ORDER_STATUS,
        default=FORMING,
    )
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ {self.user.username} №{self.id} от {self.created}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    def delete(self):
        if self.is_active:
            for item in self.orderitems.select_related():
                item.product.quantity += item.quantity
                item.product.save()
            self.is_active = False
            self.save()


class OrderItem(GetItemMixin, models.Model):
    order = models.ForeignKey(
        Order,
        related_name="orderitems",
        on_delete=models.CASCADE,
        verbose_name='заказ'
    )
    product = models.ForeignKey(
        Product,
        verbose_name='продукт',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0,
    )
    fixed_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='цена',
        blank=True,
        default=0,
    )

    # @classmethod
    # def get_item(cls, pk):
    #     return cls.objects.filter(pk=pk).first()

    def get_product_cost(self):
        return self.fixed_price * self.quantity

    def set_product_fixed_price(self, price):
        if self.order.status not in self.order.ORDER_PAID_STATUSES:
            self.fixed_price = price
