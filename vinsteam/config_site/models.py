from config_site.utils import favicon_upload_to
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Config(models.Model):
    site_name = models.CharField(
        max_length=255,
        verbose_name='Название сайта',
        blank=True,
        null=True,
        help_text='Введите название сайта которе будет отображаться в письмах'
    )
    phone_number = models.CharField(
        max_length=18,
        verbose_name='Телефонный номер',
        blank=True,
        null=True,
        help_text='Телефонный номер, отображаемый на сайте'
    )
    phone_url = models.CharField(
        max_length=15,
        verbose_name='Телефон ссылка',
        blank=True,
        null=True,
        help_text='Телефонный номер, ссылка, формат: +73822908070'
    )
    phone_number_two = models.CharField(
        max_length=18,
        verbose_name='Телефонный номер - 2',
        blank=True,
        null=True,
        help_text='Телефонный номер, отображаемый на сайте'
    )
    phone_two_url = models.CharField(
        max_length=15,
        verbose_name='Телефон ссылка - 2',
        blank=True,
        null=True,
        help_text='Телефонный номер, ссылка, формат: +73822908070'
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес',
        blank=True,
        null=True,
        help_text='Адрес вашей компании или организации'
    )
    town = models.CharField(
        max_length=255,
        verbose_name='Город',
        blank=True,
        null=True,
        help_text='Город вашей компании или организации'
    )
    postal_code = models.IntegerField(
        verbose_name='Индекс',
        blank=True,
        null=True,
        help_text='Индекс вашей компании или организации'
    )
    email = models.EmailField(
        verbose_name='Email',
        blank=True,
        null=True,
        help_text='Email, на который будут приходить сообщения с сайта'
    )
    email_site = models.EmailField(
        verbose_name='Email',
        blank=True,
        null=True,
        help_text='Email, который отображается на сайте'
    )
    logo = models.ImageField(
        upload_to='media/',
        verbose_name='Логотип',
        help_text='Изображение логотипа вашей компании или организации',
        blank=True,
        null=True,
    )
    logo_two = models.ImageField(
        upload_to='media/',
        verbose_name='Логотип дополнительный',
        help_text='Изображение логотипа вашей компании или организации',
        blank=True,
        null=True,
    )
    telegram = models.CharField(
        max_length=255, verbose_name='телеграм ссылка',
        help_text='https://t.me/+88009005010',
        blank=True, null=True)
    telegram_img = models.ImageField(
        upload_to='social_icons/', verbose_name='телеграм иконка',
        blank=True, null=True)
    whatsapp = models.CharField(
        max_length=255, verbose_name='ватсап ссылка',
        help_text='https://wa.me/79521828125',
        blank=True, null=True)
    whatsapp_img = models.ImageField(
        upload_to='social_icons/', verbose_name='ватсап иконка',
        blank=True, null=True)
    instagram = models.CharField(
        max_length=255, verbose_name='инстаграм ссылка',
        blank=True, null=True)
    instagram_img = models.ImageField(
        upload_to='social_icons/', verbose_name='инстаграм иконка',
        blank=True, null=True)
    vk = models.CharField(
        max_length=255, verbose_name='вк ссылка',
        help_text='https://vk.com/account',
        blank=True, null=True)
    vk_img = models.ImageField(
        upload_to='social_icons/', verbose_name='вк иконка',
        blank=True, null=True)
    facebook = models.CharField(
        max_length=255, verbose_name='фэйсбук ссылка',
        blank=True, null=True)
    facebook_img = models.ImageField(
        upload_to='social_icons/', verbose_name='фэйбук иконка',
        blank=True, null=True)
    other = models.CharField(
        max_length=255, verbose_name='другая ссылка',
        blank=True, null=True)
    other_img = models.ImageField(
        upload_to='social_icons/', verbose_name='другая иконка',
        blank=True, null=True)
    random = models.CharField(
        max_length=255, verbose_name='другая-2 ссылка', blank=True, null=True)
    random_img = models.ImageField(
        upload_to='social_icons/', verbose_name='другая-2 иконка',
        blank=True, null=True)
    cache = models.IntegerField(
        'Кеширование',
        help_text='Указать число в секундах',
        blank=True,
        default=0
    )
    placeholder = models.ImageField(
        upload_to='media/',
        verbose_name='Заглушка',
        help_text='Изображение Заглушка вашей компании',
        blank=True,
        null=True,
    )
    content = CKEditor5Field(
        blank=True, null=True, verbose_name='Контент')

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return self.site_name


class Config_seo(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название компании',
        blank=True,
        null=True)
    meta_description = models.TextField(
        max_length=255,
        verbose_name='Короткое описание',
        blank=True,
        null=True)
    reviews_meta_title = models.CharField(
        max_length=255,
        verbose_name='Title отзывы',
        blank=True,
        null=True)
    reviews_meta_description = models.TextField(
        max_length=255,
        verbose_name='meta_description отзывы',
        blank=True,
        null=True)
    catalog_meta_title = models.CharField(
        max_length=255,
        verbose_name='Catalog отзывы',
        blank=True,
        null=True)
    catalog_meta_description = models.TextField(
        max_length=255,
        verbose_name='meta_description catalog',
        blank=True,
        null=True)
    basket_meta_title = models.CharField(
        max_length=255,
        verbose_name='Корзина отзывы',
        blank=True,
        null=True)
    basket_meta_description = models.TextField(
        max_length=255,
        verbose_name='meta_description корзина',
        blank=True,
        null=True)
    portfolio_meta_title = models.CharField(
        max_length=255,
        verbose_name='Корзина отзывы',
        blank=True,
        null=True)
    portfolio_meta_description = models.TextField(
        max_length=255,
        verbose_name='meta_description корзина',
        blank=True,
        null=True)
    og_img = models.ImageField(
        upload_to='social_icons/',
        verbose_name='главное изо для OG',
        blank=True,
        null=True)
    favicon = models.ImageField(
        'фавикон',
        help_text='формат PNG размер 512х512',
        upload_to=favicon_upload_to,
        null=True, blank=True)
    yandex_id = models.IntegerField(
        'Номер счетчика яндекс метрика',
        default=0,
    )
    yandex_webvisor = models.BooleanField(
        default=False,
        verbose_name='Включить вебвизор яндекс')

    class Meta:
        verbose_name = 'Настройки seo'
        verbose_name_plural = 'Настройки seo'

    def __str__(self):
        return self.title


class City(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название города')

    class Meta:
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name
