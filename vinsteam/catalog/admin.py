from catalog.models import (Brand, Category, CategoryImage, FavoriteProduct,
                            Portfolio, PortfolioImage, Product, ProductImage,
                            Sale)
from django import forms
from django.contrib import admin
from django.forms import inlineformset_factory
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from mptt.admin import DraggableMPTTAdmin
from reversion.admin import VersionAdmin


class BaseImageForm(forms.ModelForm):
    class Meta:
        fields = ['image']


class ProductImageForm(BaseImageForm):
    class Meta(BaseImageForm.Meta):
        model = ProductImage


class CategoryImageForm(BaseImageForm):
    class Meta(BaseImageForm.Meta):
        model = CategoryImage


ProductImageFormSet = inlineformset_factory(
    Product, ProductImage, form=ProductImageForm, extra=1, max_num=10
)


CategoryImageFormSet = inlineformset_factory(
    Category, CategoryImage, form=CategoryImageForm, extra=1, max_num=10
)


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    formset = ProductImageFormSet


class CategoryImageAdmin(admin.TabularInline):
    model = CategoryImage
    formset = CategoryImageFormSet


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin, VersionAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'is_published',
        'id',
        'show_on_homepage',
        'is_menu',
        'slug',
        'order_on_homepage',
        'order_is_menu')
    list_display_links = ('indented_title',)
    list_filter = ['parent',]
    search_fields = ['title',]
    list_editable = (
        'order_on_homepage',
        'slug',
        'is_menu',
        'order_is_menu',
        'is_published',
        'show_on_homepage')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['parent',]
    inlines = [CategoryImageAdmin]

    fieldsets = [
        ('Основные данные', {
            'fields': (
                'title',
                'slug',
                'is_published',
                'title_menu',
                'title_catalog',
                'image',
                'image_catalog',
                'show_on_homepage',
                'image_placeholder',
                'parent',
                'short_description',
                'description',
                'image_catalog_temp',
                'order_on_homepage',
                'is_menu',
                'order_is_menu',
                'content_ckeditor',
            )
        }),
        ('SEO', {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_canonical',
                'meta_keywords',
            )
        }),
    ]

    class Media:
        js = ('js/admin_js.js',)

    def indented_title(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.title,
        )
    indented_title.short_description = _('Indented Title')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(VersionAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = (
        'title',
        'id',
        'slug',
        'is_published',
        'category',
        'show_on_homepage',
        'counter',
        'price',
        'get_image',
        'order_is_menu')
    list_filter = ('category',)
    list_editable = (
        'order_is_menu',
        'is_published',
        'category',
        'slug',
        'show_on_homepage')
    search_fields = ['title', 'description', 'category__title', 'brand__title']
    inlines = [ProductImageAdmin]
    autocomplete_fields = ['category',]
    fieldsets = [
        ('Основные данные', {
            'fields': (
                'title',
                'slug',
                'title_catalog',
                'image',
                'image_catalog',
                'show_on_homepage',
                'order_on_homepage',
                'content_ckeditor',
                'is_published',
                'counter',
                'description',
                'short_description',
                'price',
                'weight_unit',
                'category',
                'brand',
                'order_is_menu',
            )
        }),
        ('SEO', {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_canonical',
                'meta_keywords'
            )
        }),
    ]

    def view_on_site(self, obj):
        return reverse('catalog_url:product_detail', args=[obj.slug])

    def get_image(self, obj):
        if obj.images.exists():
            image_url = obj.images.first().image.url
            return format_html('<img src="{}" width="50px" />', image_url)
        else:
            return '-'

    get_image.short_description = 'Изображение'

    class Media:
        js = ('js/admin_js.js',)


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ['user']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'price_sale')


class PortfolioImageForm(forms.ModelForm):
    class Meta:
        model = PortfolioImage
        fields = ['image', 'order']


ProductImageFormSet = inlineformset_factory(
    Portfolio, PortfolioImage, form=PortfolioImageForm, extra=1, max_num=10)


class PortfolioImageAdmin(admin.TabularInline):
    model = PortfolioImage
    formset = ProductImageFormSet


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'id')
    search_fields = ('title',)
    autocomplete_fields = ['category', 'product']
    inlines = [PortfolioImageAdmin]

    class Media:
        js = ('js/admin_js.js',)
