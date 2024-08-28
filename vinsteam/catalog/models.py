from config_site.models import Config
from django.conf import settings
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from main.models import AbstractPost, MetaTagsMixin, Seo
from mptt.models import MPTTModel, TreeForeignKey
from sorl.thumbnail.shortcuts import get_thumbnail
from users.models import User


class Category(MPTTModel, AbstractPost):
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children',
        verbose_name='Родительская категория')
    show_on_homepage = models.BooleanField(
        default=False, verbose_name='Показывать на главной странице')
    order_on_homepage = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок на главной странице')
    order_is_menu = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок в меню')
    image_placeholder = models.ImageField(
        upload_to='category_images/',
        blank=True,
        null=True,
        verbose_name='Изображение заглушка')
    image_catalog_temp = models.ImageField(
        upload_to='temp_images/',
        blank=True,
        null=True,
        help_text='оно будет показываться пока не появиться основное',
        verbose_name='Изображение в каталоге временное')
    is_menu = models.BooleanField(
        'Показывать в вверхнем меню',
        default=False,
    )

    class Meta:
        verbose_name_plural = 'Категории'
        ordering = ['order_on_homepage']

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    def get_template_path(self):
        return f'catalog/category_{self.template}.html'

    def has_children(self):
        return self.get_descendants().exists()

    def get_absolute_url(self):
        return reverse('catalog_url:category_detail', args=[str(self.slug)])

    def get_image_catalog(self):
        if self.image_catalog:
            im = get_thumbnail(
                self.image_catalog, '75', format="WEBP", quality=85)
            return im.url
        parent = self.get_root()
        if parent and parent.image_placeholder:
            parent_im = get_thumbnail(
                parent.image_placeholder, '75', format="WEBP", quality=85)
            return parent_im.url
        config = Config.objects.first()
        if config.placeholder:
            config_im = get_thumbnail(
                config.placeholder, '75', format="WEBP", quality=85)
            return config_im.url
        return None


class Brand(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название бренда')

    class Meta:
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.title


class Product(AbstractPost):
    WEIGHT_CHOICES = (
        ('th', 'шт'),
        ('gr', 'гр'),
        ('m', 'm2'),
    )
    counter = models.PositiveIntegerField('Популярность', default=0)
    price = models.DecimalField(
        max_digits=8, decimal_places=0,
        verbose_name='Цена',
        null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        null=False,
        related_name='products',
        verbose_name='Категория')
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Бренд')
    weight_unit = models.CharField(
        max_length=2,
        choices=WEIGHT_CHOICES,
        default='th',
    )
    show_on_homepage = models.BooleanField(
        default=False, verbose_name='Показывать на гл. странице')
    order_on_homepage = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок на главной странице')
    order_is_menu = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок в меню')

    class Meta:
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog_url:product_detail', args=[str(self.slug)])

    def get_image_catalog(self):
        if self.image_catalog:
            im = get_thumbnail(
                self.image_catalog, '75', format="WEBP", quality=85)
            return im.url
        parent = self.category.get_root()
        if parent and parent.image_placeholder:
            parent_im = get_thumbnail(
                parent.image_placeholder, '75', format="WEBP", quality=85)
            return parent_im.url
        config = Config.objects.first()
        if config.placeholder:
            config_im = get_thumbnail(
                config.placeholder, '75', format="WEBP", quality=85)
            return config_im.url
        return None

    def get_template_path(self):
        return f'catalog/product_{self.template}.html'

    def get_weight_unit_display(self):
        display_value = dict(self.WEIGHT_CHOICES).get(self.weight_unit, '')
        if self.weight_unit == 'm':
            # Форматируем значение для 'm2', чтобы '2' было в верхнем регистре
            return 'м<sup>2</sup>'
        return display_value

    def get_price_for_city(self):
        return self.price

    def get_first_image(self):
        first_image = self.images.first()
        if first_image:
            return first_image.image
        return None


class Price(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='price_user',)
    price = models.DecimalField(max_digits=8, decimal_places=2)


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} - {self.product.title}'


class Sale(models.Model):
    WEIGHT_CHOICES = (
        ('th', 'шт'),
        ('gr', 'гр'),
        ('m', 'm2'),
    )
    title = models.CharField(
        'Название',
        max_length=255,
        null=True, blank=True
        )
    image = models.ImageField(upload_to='sales', verbose_name='Изображение')
    price = models.DecimalField(
        'Цена',
        max_digits=8, decimal_places=0)
    price_sale = models.DecimalField(
        '% скидки',
        max_digits=8,
        decimal_places=0,
        null=True, blank=True
        )
    text_price = models.CharField(
        'Единица измерения',
        max_length=255,
        null=True, blank=True,
        help_text='к примеру: м²'
        )
    weight_unit = models.CharField(
        'Единица измерения',
        max_length=2,
        choices=WEIGHT_CHOICES,
        default='th',
    )
    link = models.CharField(
        'Ссылка на запись или новость',
        max_length=255,
        blank=True)
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок')

    class Meta:
        verbose_name = 'Акции'
        verbose_name_plural = 'Акции'
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_weight_unit_display(self):
        display_value = dict(self.WEIGHT_CHOICES).get(self.weight_unit, '')
        if self.weight_unit == 'm':
            # Форматируем значение для 'm2', чтобы '2' было в верхнем регистре
            return 'м<sup>2</sup>'
        return display_value


class Portfolio(Seo, MetaTagsMixin):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='category_portfolio',
        verbose_name='Категория')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='product_portfolio',
        verbose_name='Продукт')
    title = models.CharField(
        max_length=255, verbose_name='Название')
    image_catalog = models.ImageField(
        upload_to='product_images/',
        blank=True,
        null=True,
        verbose_name='Изображение в каталоге')
    slug = models.SlugField(
        max_length=255, unique=True, verbose_name='URL')
    description = models.TextField(
        verbose_name='Описание',
        help_text='Будет показано в каталоге',
        blank=True, null=True)
    content_ckeditor = CKEditor5Field(
        blank=True, null=True, verbose_name='Контент')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата изменения')
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок')

    class Meta:
        verbose_name_plural = 'Портфолио'
        verbose_name = 'Портфолио'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog_url:portfolio_detail', args=[str(self.slug)])


class BaseImage(models.Model):
    image = models.ImageField(upload_to='products', verbose_name='Изображение')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        abstract = True
        ordering = ['order']


class ProductImage(BaseImage):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'


class CategoryImage(BaseImage):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='images')

    class Meta:
        verbose_name = 'Изображение категории'
        verbose_name_plural = 'Изображения категории'


class PortfolioImage(BaseImage):
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='images')

    class Meta:
        verbose_name = 'Изображение портфолио'
        verbose_name_plural = 'Изображения портфолио'
