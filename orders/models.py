from django.db import models
from django.conf import settings
from django.urls import reverse
from games.models import Game


class Order(models.Model):
    """
    Модель заказа.
    Хранит информацию о покупателе, сумме и статусе заказа.
    """
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь',
        null=True,
        blank=True
    )
    email = models.EmailField('Email для доставки ключа')
    total_price = models.DecimalField(
        'Сумма заказа',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.id} ({self.email})'

    def get_absolute_url(self):
        return reverse('orders:order_detail', kwargs={'order_id': self.id})


class OrderItem(models.Model):
    """
    Позиция в заказе.
    Связывает заказ с конкретной игрой и фиксирует цену на момент покупки.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,  
        related_name='order_items',
        verbose_name='Игра'
    )
    price = models.DecimalField('Цена на момент покупки', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return f'{self.game.title} в заказе #{self.order.id}'