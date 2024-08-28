from articles.mixins import MenuView
from articles.models import Head, Page, Post
from asgiref.sync import sync_to_async
from banner.models import Slider
from catalog.mixins import (BasketProductsMixin, FavoriteProductsMixin,
                            MainCategoriesMixin)
from catalog.models import Portfolio, Product
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.cache import caches
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from mail_post.views import FeedView
from reviews.mixins import ReviewMixin
from users.mixins import RegistrForm


@sync_to_async
def check_user_authenticated(request):
    return request.user.is_authenticated


class BaseMixin(
        MainCategoriesMixin,
        FavoriteProductsMixin,
        BasketProductsMixin,
        MenuView,
        FeedView,
        RegistrForm
        ):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IndexView(
        BaseMixin,
        ReviewMixin,
        TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sliders = Slider.objects.filter(
            is_active=True).order_by('order')
        products_hits = Product.objects.filter(
            category_id=1).order_by('-counter')[:6]
        page = get_object_or_404(Page, is_homepage=True)
        posts = Post.objects.filter(
            category__id=1, is_published=True).order_by('-pk')[:3]
        category = get_object_or_404(Head, id=1)
        category_posts = category.slug
        content_blocks = page.content_blocks.all()
        enabled_reviews = self.get_enabled_reviews()[:8]
        portfolios = Portfolio.objects.all()[:8]
        context.update(
                sliders=sliders,
                posts=posts,
                category_posts=category_posts,
                page=page,
                portfolios=portfolios,
                products_hits=products_hits,
                content_blocks=content_blocks,
                enabled_reviews=enabled_reviews,
                meta_tags=page.get_meta_tags()
                )
        return context


def paginator_page(request, page_pagi):
    paginator = Paginator(page_pagi, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


@login_required
@staff_member_required
@require_GET
def clear_cache(request):
    cache = caches['default']
    cache.clear()
    return redirect('main_url:main_index')


@login_required
@staff_member_required
@require_GET
def clear_session(request):
    cache = caches['sessions']
    cache.clear()
    return redirect('main_url:main_index')
