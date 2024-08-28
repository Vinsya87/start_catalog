from catalog.models import Product
from django.core.validators import MinValueValidator
from django.db import models
from users.models import Address, User


class BasketProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1, verbose_name='Количество',
        validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('user', 'product')
        verbose_name_plural = 'Корзина'

    def __str__(self):
        if self.user and self.user.username:
            return f'{self.user.username} - {self.product.title}'
        return f'Anonymous - {self.product.title}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('Ожидание', 'Ожидание'),
        ('В работе', 'В работе'),
        ('Выполнен', 'Выполнен'),
    ]
    TIME_RANGE_CHOICES = [
        ('Утро', 'Утро (9:00 - 12:00)'),
        ('День', 'День (12:00 - 15:00)'),
        ('Вечер', 'Вечер (15:00 - 18:00)'),
    ]
    time_range = models.CharField(
        max_length=10,
        choices=TIME_RANGE_CHOICES,
        default='Утро',
        verbose_name='Временной диапазон')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        blank=True,
        null=True,)
    name = models.CharField(max_length=255, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(max_length=255, verbose_name='Почта')
    delivery_date = models.DateField(
        verbose_name='Дата доставки',
        null=True,
        blank=True,
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name='Итоговая цена')
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        # limit_choices_to={'user': models.OuterRef('user')}
    )
    message = models.TextField(
        verbose_name='Сообщение',
        blank=True)
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Ожидание')

    class Meta:
        verbose_name_plural = 'Заказ'
        verbose_name = 'Заказы'

    def get_time_range_display(self):
        return dict(self.TIME_RANGE_CHOICES).get(
            self.time_range, self.time_range)

    def calculate_total_price(self):
        """
        Метод для расчета итоговой цены заказа.
        """
        total_price = 0
        for item in self.items.all():
            product_price_for_city = item.product.price
            if product_price_for_city is not None:
                total_price += item.quantity * product_price_for_city
            else:
                # Цена для данного товара в данном городе не указана,
                # обработайте эту ситуацию по вашему усмотрению
                pass
        self.total_price = total_price
        self.save()

    def __str__(self):
        return f"Заказ #{self.id} - {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name='items',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        related_name='orders',
        on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        'Количество',
        default=1)
    city_price = models.DecimalField(
        max_digits=10,
        verbose_name='Цена',
        decimal_places=2,
        blank=True,
        null=True
        )

    class Meta:
        unique_together = [['order', 'product']]
        verbose_name_plural = 'Заказ - юзер'
        verbose_name = 'Заказы - юзера'

    def __str__(self):
        return f"Заказ {self.order}"
