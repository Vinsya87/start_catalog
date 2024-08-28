from catalog.models import Category, FavoriteProduct, Portfolio, Product
from config_site.models import Config_seo
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import aget_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import View
from main.views import BaseMixin, check_user_authenticated
from reviews.mixins import ReviewMixin
from reviews.models import ReviewProduct


class CategoryDetailView(
        BaseMixin,
        DetailView):
    model = Category
    context_object_name = 'category_product'
    slug_url_kwarg = 'slug'

    def get_template_names(self):
        instance = self.get_object()
        template_path = instance.get_template_path()
        return [template_path]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_product = self.get_object()
        categories = Category.objects.filter(parent=None)
        show_sort = self.request.GET.get('show_sort', 'popularity')
        show_count = self.request.GET.get('show_count', 15)
        product_list = Product.objects.filter(category=category_product)

        # Сортировка товаров
        if show_sort == 'price_asc':
            product_list = product_list.order_by('price')
        elif show_sort == 'price_desc':
            product_list = product_list.order_by('-price')
        elif show_sort == 'popularity':
            product_list = product_list.order_by('-counter')
        # Пагинация
        paginator = Paginator(product_list, show_count)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if hasattr(self.object, 'get_meta_tags'):
            context['meta_tags'] = self.object.get_meta_tags()

        context['categories'] = categories
        context['page_obj'] = page_obj
        context['show_sort'] = show_sort
        context['show_count'] = show_count
        context['category_product'] = category_product
        context['has_children'] = category_product.has_children()
        context['subcategories'] = category_product.get_descendants()
        return context


class CategoryAllView(
        BaseMixin,
        ListView):
    model = Category
    template_name = 'catalog/category_all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(parent=None)
        context['categories'] = categories
        context['catalog'] = True
        config_seo = Config_seo.objects.first()
        context['meta_title'] = config_seo.catalog_meta_title
        context['meta_description'] = config_seo.catalog_meta_description
        return context


class ProductDetailView(
        BaseMixin,
        ReviewMixin,
        DetailView):
    model = Product
    context_object_name = 'product'

    def get_template_names(self):
        instance = self.get_object()
        template_path = instance.get_template_path()
        return [template_path]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        category = product.category
        product = context['product']
        if hasattr(self.object, 'get_meta_tags'):
            context['meta_tags'] = self.object.get_meta_tags()
        categories = Category.objects.filter(parent=None)
        # Получение хитовых продуктов
        hit_products = (
            Product.objects.filter(category=category)
            .exclude(id=product.id)
            .order_by('-counter')[:4]
        )
        enabled_reviews = ReviewProduct.objects.filter(
            product=product, is_enabled=True)
        context['hit_products'] = hit_products
        context['enabled_reviews'] = enabled_reviews
        context['product'] = product
        context['categories'] = categories
        return context


class AddToFavoriteView(View):
    http_method_names = ['post']

    async def post(self, request, pk):
        product = await aget_object_or_404(Product, pk=pk)
        session_key = request.session.session_key
        if await check_user_authenticated(request):
            try:
                favorite_product = await FavoriteProduct.objects.aget(
                    user=request.user, product=product)
                await favorite_product.adelete()
                added = False
            except FavoriteProduct.DoesNotExist:
                favorite_product = await FavoriteProduct.objects.acreate(
                    user=request.user, product=product)
                added = True
        else:
            favorites = await cache.aget(f'favorites:{session_key}')
            if not favorites:
                favorites = set()
            else:
                favorites = set(favorites)
            if pk not in favorites:
                favorites.add(pk)
                await cache.aset(f'favorites:{session_key}', favorites)
                added = True
            else:
                favorites.remove(pk)
                await cache.aset(f'favorites:{session_key}', favorites)
                added = False
        return JsonResponse({'added': added})


class SearchView(
        BaseMixin,
        TemplateView):
    template_name = 'catalog/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        product_list = None
        if query:
            product_list = Product.objects.filter(
                Q(title__icontains=query) |
                Q(title__icontains=query.lower()) |
                Q(title__icontains=query.capitalize()))
            categories = Category.objects.filter(parent=None)
            show_count = self.request.GET.get('show_count', 15)
            show_sort = self.request.GET.get('show_sort', 'popularity')
            context.update({
                    'title': f'Поиск по "{query}"',
                    'categories': categories,
                    'show_sort': show_sort,
                    'show_count': show_count,
                    'query': query,
                    })
            if product_list.exists():
                if show_sort == 'price_asc':
                    product_list = product_list.order_by('price')
                elif show_sort == 'price_desc':
                    product_list = product_list.order_by('-price')
                elif show_sort == 'popularity':
                    product_list = product_list.order_by('-counter')
                paginator = Paginator(product_list, show_count)
                page_number = self.request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                context.update({
                    'products': product_list,
                    'page_obj': page_obj,
                })
            else:
                context.update({
                    'message': 'Поиск не дал результатов',
                })
        return context


class FavoriteView(
        BaseMixin,
        ListView):
    template_name = 'catalog/favorites.html'
    model = FavoriteProduct
    context_object_name = 'favorites'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return FavoriteProduct.objects.filter(user=self.request.user)
        else:
            session_key = self.request.session.session_key
            favorites = cache.get(f'favorites:{session_key}', set())
            favorite_products = Product.objects.filter(pk__in=favorites)
            return [
                FavoriteProduct(product=prod)
                for prod in favorite_products]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Избранное'
        products_in_favorites = [
            favorite.product for favorite in context['favorites']]
        context['products_in_favorites'] = products_in_favorites

        return context


class PortfolioListView(
        BaseMixin,
        ListView):
    model = Portfolio
    template_name = 'catalog/portfolio_list.html'
    context_object_name = 'portfolios'
    queryset = Portfolio.objects.filter(
        is_published=True).order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config_seo = Config_seo.objects.first()
        context['meta_title'] = config_seo.portfolio_meta_title
        context['meta_description'] = config_seo.portfolio_meta_description
        return context


class PortfolioDetailView(
        BaseMixin,
        DetailView):
    model = Portfolio
    template_name = 'catalog/portfolio_detail.html'
    context_object_name = 'portfolio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'get_meta_tags'):
            context['meta_tags'] = self.object.get_meta_tags()

        portfolio = self.get_object()
        count = 6

        product_portfolios = []
        if portfolio.product:
            # Сначала находим портфолио, относящиеся к тому же продукту
            product_portfolios = list(
                Portfolio.objects.filter(
                    product=portfolio.product).exclude(id=portfolio.id)[:count]
            )
            remaining_count = count - len(product_portfolios)

            if remaining_count > 0 and portfolio.product.category:
                # Затем находим портфолио, относящиеся к категории продукта данного портфолио
                category_portfolios = list(
                    Portfolio.objects.filter(
                        product__category=portfolio.product.category)
                    .exclude(id__in=[p.id for p in product_portfolios + [portfolio]])
                    [:remaining_count]
                )
                product_portfolios += category_portfolios
                remaining_count = count - len(product_portfolios)
        else:
            remaining_count = count

        if remaining_count > 0:
            # И в конце добавляем любые другие портфолио, чтобы заполнить до нужного количества
            other_portfolios = list(
                Portfolio.objects.exclude(
                    id__in=[p.id for p in product_portfolios + [portfolio]]
                    )[:remaining_count]
            )
            product_portfolios += other_portfolios

        portfolios = product_portfolios[:count]
        context['portfolios'] = portfolios

        return context
