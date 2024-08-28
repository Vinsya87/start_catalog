from articles.models import Head, Page, Post
from catalog.models import Category as CategoryProduct
from catalog.models import Product
from django.contrib.sitemaps import Sitemap


class CategoryProductSitemap(Sitemap):
    def items(self):
        return CategoryProduct.objects.filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()


class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()


class PageSitemap(Sitemap):
    def items(self):
        return Page.objects.filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()


class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()


class HeadSitemap(Sitemap):
    def items(self):
        return Head.objects.filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()
