from django.contrib import admin
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Message(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    post = models.CharField(
        max_length=255, verbose_name='Проект',
        blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name='E-mail')
    phone_number = PhoneNumberField(verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.name


class Spam(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField(blank=True, null=True, verbose_name='E-mail')
    phone_number = PhoneNumberField(verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Спам'
        verbose_name_plural = 'Спам'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            # Проверяем общее количество записей
            if Spam.objects.count() >= 100:
                # Если количество записей превышает 100, удаляем самую старую запись
                oldest_spam = Spam.objects.order_by('created_at').first()
                oldest_spam.delete()
        super().save(*args, **kwargs)