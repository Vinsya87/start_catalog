from articles.models import Head, MenuItem, Page, Post, Submenu
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from django.forms import Textarea, inlineformset_factory
from django.urls import reverse
from main.models import ContentBlock, Image, ImageBlock
from reversion.admin import VersionAdmin

admin.site.site_header = "Панель управления"
admin.site.site_title = "Админка сайта"


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


ProductImageFormSet = inlineformset_factory(
    ImageBlock, Image, form=ProductImageForm, extra=1, max_num=10)


class ProductImageAdmin(admin.TabularInline):
    model = Image
    formset = ProductImageFormSet


class ImageBlockInline(admin.StackedInline):
    model = Page.image_blocks.through
    extra = 1
    verbose_name_plural = 'Блоки галерии на странице'


class PageBlockInline(admin.TabularInline):
    model = Page.content_blocks.through
    verbose_name_plural = 'Блоки контента на странице'
    extra = 1


@admin.register(Head)
class HeadAdmin(VersionAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'id')
    search_fields = ('title',)

    class Media:
        js = ('js/admin_js.js',)


class PostBlockInline(admin.TabularInline):
    model = Post.content_blocks.through
    verbose_name_plural = 'Блоки контента на записи'


class PostAdmin(VersionAdmin):
    list_display = (
        'title', 'category', 'is_published',
        'order', 'slug', 'created_at')
    list_filter = ('category', 'created_at')
    list_editable = ('slug', 'order', 'is_published')
    search_fields = ('title', 'content_ckeditor')
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 5, 'cols': 40})},
    }

    fieldsets = [
        ('Основные данные', {'fields': (
            'title',
            'slug',
            'template',
            'is_published',
            'short_description',
            'category',
            'main_content_block',
            'slider',
            'content_ckeditor',
         'image', 'created_at', 'order')}),
        ('SEO', {'fields': ('meta_title',
                            'meta_description',
                            'meta_canonical',
                            'meta_keywords')}),
    ]

    inlines = [PostBlockInline]

    class Media:
        js = ('js/admin_js.js',)

    def view_on_site(self, obj):
        return reverse('articles:post_detail', args=[obj.slug])

    list_display_links = ('title', 'category')


admin.site.register(Post, PostAdmin)


class ContentBlockInlineForm(forms.ModelForm):
    class Meta:
        model = ContentBlock
        fields = ['title', 'content_ckeditor', 'css_class', 'div_id']


class ContentBlockInlineWidget(forms.ModelChoiceField):
    widget = forms.Select(attrs={'class': 'content-block-inline'})


@admin.register(Page)
class PageAdmin(VersionAdmin):
    list_display = ('title', 'is_homepage',
                    'is_published', 'slug',
                    'id', 'created_at')
    list_editable = ('slug', 'is_published')
    list_filter = ('created_at',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    inlines = [
        PageBlockInline,
        ImageBlockInline,
        ]

    fieldsets = [
        ('Основные данные', {'fields': (
            'title',
            'is_homepage',
            'slider',
            'template',
            'is_published',
            'slug',
            'content_ckeditor')}),
        ('SEO', {'fields': (
            'meta_title',
            'meta_description',
            'meta_canonical',
            'meta_keywords')})
    ]
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 5, 'cols': 40})},
    }

    class Media:
        js = ('js/admin_js.js',)

    def view_on_site(self, obj):
        return reverse('articles:page_detail', args=[obj.slug])


@admin.register(MenuItem)
class MenuItemAdmin(VersionAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple(
            verbose_name='Подменю',
            is_stacked=False)},
    }
    list_display = (
        'title',
        'url',
        'order',
        'is_active',
        'is_main_menu',
        'is_mobile_menu',
        'is_footer_menu',
        'is_other_menu')
    list_editable = (
        'url',
        'order',
        'is_active',
        'is_main_menu',
        'is_mobile_menu',
        'is_footer_menu',
        'is_other_menu')
    search_fields = ('title', 'url')


@admin.register(Submenu)
class SubmenuAdmin(VersionAdmin):
    list_display = (
        'title', 'url',
        'order', 'is_active',
        )
    list_editable = (
        'url', 'order',
        'is_active')


@admin.register(ContentBlock)
class ContentBlockAdmin(VersionAdmin):
    list_display = ('title', 'number', 'css_class', 'div_id')


@admin.register(ImageBlock)
class ImageBlockAdmin(VersionAdmin):
    list_display = ('title', 'order')
    inlines = [ProductImageAdmin]
    list_editable = ('order',)
