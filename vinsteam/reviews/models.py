from catalog.models import Product
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class AbstractReview(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField(blank=True, verbose_name='Email')
    phone = PhoneNumberField(
        null=True, blank=True,
        verbose_name='Телефон',
        error_messages={
            'invalid': 'Пожалуйста, введите корректный номер телефона'})
    text = models.TextField(verbose_name='Отзыв')
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания')
    is_enabled = models.BooleanField(
        default=False, verbose_name='Включить отзыв')

    class Meta:
        abstract = True


class Review(AbstractReview):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.name

    @property
    def text_length(self):
        return len(self.text)


class ReviewProduct(AbstractReview):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name = 'Отзыв к товару'
        verbose_name_plural = 'Отзывы к товарам'

    def __str__(self):
        return self.name

    @property
    def text_length(self):
        return len(self.text)
