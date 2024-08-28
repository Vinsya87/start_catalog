from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from main.models import AbstractPost, ContentBlock


class Head(AbstractPost):
    blog = models.BooleanField(
        'Блог',
        default=False)

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:post_list_by_category', args=[str(self.slug)])

    def get_template_path(self):
        return f'articles/article_{self.template}.html'


class Post(AbstractPost):
    category = models.ForeignKey(
        Head,
        on_delete=models.PROTECT,
        related_name='posts',
        verbose_name='Рубрика',
        null=False
    )
    main_content_block = models.ForeignKey(
        ContentBlock,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='main_post_content',
        verbose_name='Главный блок контента'
    )

    class Meta:
        verbose_name_plural = 'Записи'
        verbose_name = 'Запись'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_template_path(self):
        return f'articles/post_{self.template}.html'

    def get_absolute_url(self):
        return reverse('articles:post_detail', args=[str(self.slug)])


class Page(AbstractPost):
    is_homepage = models.BooleanField(
        default=False,
        verbose_name='Главная страница')
    main_content_block = models.ForeignKey(
        ContentBlock,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='main_page_content',
        verbose_name='Главный блок контента'
    )

    class Meta:
        verbose_name_plural = 'Страницы'
        verbose_name = 'Страница'

    def __str__(self):
        return self.title

    def get_template_path(self):
        return f'articles/page_{self.template}.html'

    def get_absolute_url(self):
        if self.is_homepage:
            return reverse('main_url:main_index')
        else:
            return reverse('articles:page_detail', args=[str(self.slug)])


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name='Включить меню')
    is_main_menu = models.BooleanField(
        default=False, verbose_name='Главное меню')
    is_mobile_menu = models.BooleanField(
        default=False, verbose_name='Мобильное меню')
    is_footer_menu = models.BooleanField(
        default=False, verbose_name='Футер меню')
    is_other_menu = models.BooleanField(
        default=False, verbose_name='Другое меню')
    category = models.ForeignKey(
        Head,
        on_delete=models.PROTECT,
        related_name='menu_items',
        verbose_name='Рубрика',
        null=True, blank=True,
        help_text=('можно указать рубрику, и будут выведены все записи из нее')
        )
    submenus = models.ManyToManyField(
        'Submenu',
        related_name='menu_items',
        verbose_name='Подменю',
        blank=True,
        help_text='Выберите подменю, которые будут содержаться в этом меню'
    )

    class Meta:
        ordering = ('order',)
        verbose_name_plural = 'Меню'
        verbose_name = 'Меню'

    def __str__(self):
        return self.title


class Submenu(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name='Включить меню')
    category = models.ForeignKey(
        Head,
        on_delete=models.PROTECT,
        related_name='submenu_items',
        verbose_name='Рубрика',
        null=True, blank=True,
        help_text=('можно указать рубрику, и будут выведены все записи из нее')
        )

    class Meta:
        ordering = ('order',)
        verbose_name_plural = 'Подменю'
        verbose_name = 'Подменю'

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Page)
def update_homepage(sender, instance, **kwargs):
    if instance.is_homepage:
        # Убедиться, что только одна страница может быть отмечена как главная
        Page.objects.exclude(pk=instance.pk).update(is_homepage=False)
