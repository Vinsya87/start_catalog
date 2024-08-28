# Generated by Django 5.1 on 2024-08-26 08:33

import django.db.models.deletion
import django.utils.timezone
import django_ckeditor_5.fields
import main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('banner', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Head',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_canonical', models.CharField(blank=True, max_length=255, null=True, verbose_name='Canonical')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta Title')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Meta Description')),
                ('meta_keywords', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta Keywords')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('template', models.CharField(choices=[('template', 'Шаблон основной'), ('template_1', 'Шаблон - 1'), ('template_2', 'Шаблон - 2')], default='template', max_length=15, verbose_name='Шаблон')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('title_menu', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название в меню')),
                ('title_catalog', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название в каталоге')),
                ('short_description', models.TextField(blank=True, null=True, verbose_name='Короткое описание')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('content_ckeditor', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Контент')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Сортировка')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Изображение')),
                ('image_catalog', models.ImageField(blank=True, null=True, upload_to='catalog_images/', verbose_name='Изображение в каталоге')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата изменения')),
                ('content_blocks', models.ManyToManyField(blank=True, to='main.contentblock', verbose_name='Блоки контента')),
                ('image_blocks', models.ManyToManyField(blank=True, to='main.imageblock', verbose_name='Изображения записи или страницы')),
                ('slider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='banner.slider', verbose_name='Слайдер на странице')),
            ],
            options={
                'verbose_name': 'Рубрика',
                'verbose_name_plural': 'Рубрики',
            },
            bases=(models.Model, main.models.MetaTagsMixin),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_canonical', models.CharField(blank=True, max_length=255, null=True, verbose_name='Canonical')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta Title')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Meta Description')),
                ('meta_keywords', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta Keywords')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('template', models.CharField(choices=[('template', 'Шаблон основной'), ('template_1', 'Шаблон - 1'), ('template_2', 'Шаблон - 2')], default='template', max_length=15, verbose_name='Шаблон')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('title_menu', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название в меню')),
                ('title_catalog', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название в каталоге')),
                ('short_description', models.TextField(blank=True, null=True, verbose_name='Короткое описание')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('content_ckeditor', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Контент')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Сортировка')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Изображение')),
                ('image_catalog', models.ImageField(blank=True, null=True, upload_to='catalog_images/', verbose_name='Изображение в каталоге')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата изменения')),
                ('is_homepage', models.BooleanField(default=False, verbose_name='Главная страница')),
                ('content_blocks', models.ManyToManyField(blank=True, to='main.contentblock', verbose_name='Блоки контента')),
                ('image_blocks', models.ManyToManyField(blank=True, to='main.imageblock', verbose_name='Изображения записи или страницы')),
                ('main_content_block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_page_content', to='main.contentblock', verbose_name='Главный блок контента')),
                ('slider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='banner.slider', verbose_name='Слайдер на странице')),
            ],
            options={
                'verbose_name': 'Страница',
                'verbose_name_plural': 'Страницы',
            },
            bases=(models.Model, main.models.MetaTagsMixin),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_canonical', models.CharField(blank=True, max_length=255, null=True, verbose_name='Canonical')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta Title')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Meta Description')),
                ('meta_keywords', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta Keywords')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('template', models.CharField(choices=[('template', 'Шаблон основной'), ('template_1', 'Шаблон - 1'), ('template_2', 'Шаблон - 2')], default='template', max_length=15, verbose_name='Шаблон')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('title_menu', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название в меню')),
                ('title_catalog', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название в каталоге')),
                ('short_description', models.TextField(blank=True, null=True, verbose_name='Короткое описание')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('content_ckeditor', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Контент')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Сортировка')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Изображение')),
                ('image_catalog', models.ImageField(blank=True, null=True, upload_to='catalog_images/', verbose_name='Изображение в каталоге')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата изменения')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='articles.head', verbose_name='Рубрика')),
                ('content_blocks', models.ManyToManyField(blank=True, to='main.contentblock', verbose_name='Блоки контента')),
                ('image_blocks', models.ManyToManyField(blank=True, to='main.imageblock', verbose_name='Изображения записи или страницы')),
                ('main_content_block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_post_content', to='main.contentblock', verbose_name='Главный блок контента')),
                ('slider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='banner.slider', verbose_name='Слайдер на странице')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
                'ordering': ['-created_at'],
            },
            bases=(models.Model, main.models.MetaTagsMixin),
        ),
        migrations.CreateModel(
            name='Submenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.CharField(blank=True, max_length=255)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True, verbose_name='Включить меню')),
                ('category', models.ForeignKey(blank=True, help_text='можно указать рубрику, и будут выведены все записи из нее', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='submenu_items', to='articles.head', verbose_name='Рубрика')),
            ],
            options={
                'verbose_name': 'Подменю',
                'verbose_name_plural': 'Подменю',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.CharField(blank=True, max_length=255)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True, verbose_name='Включить меню')),
                ('is_main_menu', models.BooleanField(default=False, verbose_name='Главное меню')),
                ('is_mobile_menu', models.BooleanField(default=False, verbose_name='Мобильное меню')),
                ('is_footer_menu', models.BooleanField(default=False, verbose_name='Футер меню')),
                ('is_other_menu', models.BooleanField(default=False, verbose_name='Другое меню')),
                ('category', models.ForeignKey(blank=True, help_text='можно указать рубрику, и будут выведены все записи из нее', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='menu_items', to='articles.head', verbose_name='Рубрика')),
                ('submenus', models.ManyToManyField(blank=True, help_text='Выберите подменю, которые будут содержаться в этом меню', related_name='menu_items', to='articles.submenu', verbose_name='Подменю')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
                'ordering': ('order',),
            },
        ),
    ]
