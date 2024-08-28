from banner.models import Slider
from config_site.models import Config_seo
from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class Seo(models.Model):
    meta_canonical = models.CharField(
        max_length=255, blank=True,
        null=True, verbose_name='Canonical')
    meta_title = models.CharField(
        max_length=255, blank=True,
        null=True, verbose_name='Meta Title')
    meta_description = models.TextField(
        blank=True, null=True, verbose_name='Meta Description')
    meta_keywords = models.CharField(
        max_length=255, blank=True,
        null=True, verbose_name='Meta Keywords')
    is_published = models.BooleanField(
        default=True, verbose_name='Опубликовано')

    class Meta:
        abstract = True
        verbose_name = 'СЕО Настройки'
        verbose_name_plural = 'СЕО Настройки'


class MetaTagsMixin:
    def get_meta_tags(self):
        config_seo = Config_seo.objects.first()
        if hasattr(self, 'meta_title') and self.meta_title:
            meta_title = self.meta_title
        else:
            meta_title = f'{self.title}'
        if hasattr(self, 'meta_description') and self.meta_description:
            meta_description = self.meta_description
        else:
            meta_description = f'{self.title}. {config_seo.meta_description}'

        return {
            'meta_title': meta_title,
            'meta_description': meta_description
        }


class ImageBlock(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    order = models.PositiveIntegerField(
        'Сортировка', default=0)

    class Meta:
        verbose_name_plural = 'Изображения страницы'
        verbose_name = 'Изображение'
        ordering = ['order']

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')
    image_block = models.ForeignKey(
        ImageBlock, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name_plural = 'Изображения'
        verbose_name = 'Изображение'

    def __str__(self):
        return str(self.image_block)


class ContentBlock(models.Model):
    title = models.CharField(
        max_length=255, blank=True,
        null=True, verbose_name='Название блока')
    number = models.PositiveIntegerField(
        unique=True, verbose_name='Номер блока')
    content_ckeditor = CKEditor5Field(verbose_name='Контент')
    css_class = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='CSS класс')
    div_id = models.CharField(
        max_length=255, unique=True, blank=True,
        null=True, verbose_name='ID div')

    class Meta:
        verbose_name_plural = 'Блоки контента'
        verbose_name = 'Блок контента'
        ordering = ['number']

    def __str__(self):
        return f'{self.title}'


class AbstractPost(Seo, MetaTagsMixin):
    TEMPLATE_CHOICES = [
        ("template", "Шаблон основной"),
        ("template_1", "Шаблон - 1"),
        ("template_2", "Шаблон - 2"),
    ]
    template = models.CharField(
        max_length=15,
        choices=TEMPLATE_CHOICES,
        default="template",
        verbose_name="Шаблон",
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    title_menu = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Название в меню')
    title_catalog = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Название в каталоге')
    short_description = models.TextField(
        verbose_name='Короткое описание',
        blank=True, null=True)
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True)
    content_ckeditor = CKEditor5Field(
        blank=True, null=True, verbose_name='Контент')
    content_blocks = models.ManyToManyField(
        ContentBlock, verbose_name='Блоки контента', blank=True)
    slider = models.ForeignKey(
        Slider,
        on_delete=models.PROTECT,
        verbose_name='Слайдер на странице',
        null=True, blank=True
    )
    order = models.PositiveIntegerField(
        'Сортировка', default=0)
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='images/',
        verbose_name='Изображение'
    )
    image_catalog = models.ImageField(
        upload_to='catalog_images/',
        blank=True,
        null=True,
        verbose_name='Изображение в каталоге')
    image_blocks = models.ManyToManyField(
        ImageBlock,
        verbose_name='Изображения записи или страницы', blank=True)
    slug = models.SlugField(
        max_length=255, unique=True, verbose_name='URL')
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(
        default=timezone.now, verbose_name='Дата изменения')

    class Meta:
        abstract = True
