from config_site.models import City
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    email = models.EmailField('Email', max_length=254, unique=True)
    is_active = models.BooleanField(
        'Доступ в лк',
        default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses')
    name = models.CharField('Название', max_length=255, blank=True)
    city = models.ForeignKey(
        City, verbose_name='Город', on_delete=models.CASCADE)
    street = models.CharField('Улица', max_length=255)
    building = models.CharField('Дом', max_length=20)
    apartment = models.CharField('Квартира', max_length=20, blank=True)

    class Meta:
        verbose_name_plural = 'Адреса'
        verbose_name = 'Адрес'
        unique_together = [[
            'user', 'city', 'street', 'building', 'apartment']]

    def __str__(self):
        return (
            f'г. - {self.street}, {self.building}'
            f'{", кв. " + self.apartment if self.apartment else ""}'
        )
