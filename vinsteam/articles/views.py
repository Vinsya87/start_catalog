from articles.models import Head, Page
from articles.models import Post as ArticlePost
from django.views.generic import DetailView, ListView
from main.views import BaseMixin


class ArticleView(BaseMixin, ListView):
    model = ArticlePost
    context_object_name = 'posts'
    template_name = 'catalog/article_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = ArticlePost.objects.all()
        return queryset


class PostDetailView(
        BaseMixin,
        DetailView):
    model = ArticlePost
    context_object_name = 'post'

    def get_template_names(self):
        instance = self.get_object()
        template_path = instance.get_template_path()
        return [template_path]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'get_meta_tags'):
            context['meta_tags'] = self.object.get_meta_tags()
        return context


class PageDetailView(
        BaseMixin,
        DetailView):
    model = Page
    context_object_name = 'page'

    def get_template_names(self):
        instance = self.get_object()
        template_path = instance.get_template_path()
        return [template_path]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'get_meta_tags'):
            context['meta_tags'] = self.object.get_meta_tags()
        return context


class PostListByCategory(
        BaseMixin,
        ListView):
    """Список постов категории"""
    model = ArticlePost
    context_object_name = 'posts'

    def get_template_names(self):
        category_slug = self.kwargs['category_slug']
        if category_slug == 'nashi-proekty':
            return ['articles/article_list_proekty.html']
        elif category_slug == 'services':
            return ['articles/art_list_services.html']
        else:
            return ['articles/article_list.html']

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = Head.objects.get(slug=category_slug)
        queryset = ArticlePost.objects.filter(
            category=category, is_published=True).order_by('order')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        category = Head.objects.get(slug=category_slug)
        context['category_articles'] = category
        if hasattr(category, 'get_meta_tags'):
            context['meta_tags'] = category.get_meta_tags()
        return context
