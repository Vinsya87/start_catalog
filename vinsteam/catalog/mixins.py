from basket.models import BasketProduct
from catalog.models import Category as ProdCategory
from catalog.models import FavoriteProduct, Product
from django.contrib.sessions.backends.file import SessionStore
from django.core.cache import cache
from django.views.generic.base import ContextMixin


class MainCategoriesMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories_all = ProdCategory.objects.filter(parent=None)
        context['categories_all'] = categories_all
        return context


class FavoriteProductsMixin(ContextMixin):
    def get_favorite_products(self):
        if self.request.user.is_authenticated:
            return FavoriteProduct.objects.filter(
                user=self.request.user).values_list('product__pk', flat=True)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                session = SessionStore()
                session.save()
                session_key = session.session_key
                self.request.session['session_key'] = session_key
            favorites = cache.get(f'favorites:{session_key}')
            if not favorites:
                favorites = set()
            favorites.update(
                Product.objects.filter(
                    pk__in=favorites).values_list('id', flat=True))
            cache.set(f'favorites:{session_key}', favorites)
            return favorites

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favorite_products = self.get_favorite_products()
        num_favorite_products = len(favorite_products)
        context['num_favorite_products'] = num_favorite_products
        if self.request.user.is_authenticated:
            context['favorite_products'] = list(favorite_products)
        else:
            context['favorite_products'] = list(favorite_products)
        return context


class BasketProductsMixin(ContextMixin):
    def get_basket_products(self):
        if self.request.user.is_authenticated:
            return BasketProduct.objects.filter(
                user=self.request.user).values_list('product__pk', flat=True)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                session = SessionStore()
                session.save()
                session_key = session.session_key
                self.request.session['session_key'] = session_key
            baskets = cache.get(f'baskets:{session_key}')
            print(baskets)
            if not baskets:
                baskets = set()
            return baskets

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basket_products = self.get_basket_products()
        num_basket_products = len(basket_products)
        context['num_basket_products'] = num_basket_products
        if self.request.user.is_authenticated:
            context['basket_products'] = list(basket_products)
        else:
            context['basket_products'] = list(basket_products)
        return context
