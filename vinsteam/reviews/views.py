from catalog.models import Product
from config_site.models import Config, Config_seo
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.views.generic import ListView
from django.views.generic.edit import FormView
from main.views import BaseMixin
from reviews.forms import ReviewForm, ReviewProductForm
from reviews.mixins import ReviewMixin
from reviews.models import Review, ReviewProduct


class AddReviewView(ReviewMixin, FormView):
    success_url = ''
    form_class = ReviewForm

    def form_valid(self, form):
        if self.request.POST.get('privacy_policy') != 'on':
            return JsonResponse({
                'success': False,
                'errors': {
                    'privacy_policy': [
                        'Подтвердите согласие с политикой безопасности']}},
                    status=400)
        review = form.save(commit=False)
        review.user = self.request.user
        review.save()
        data = {'success': True}
        config = Config.objects.first()
        recipient_list = [config.email]
        if recipient_list:
            subject = 'Смайк - Новый отзыв добавлен'
            username = self.request.POST.get('username', '')
            message = f'Новый отзыв был добавлен на сайте пользователем {username}.'
            email_from = f'Cайт - {config.site_name} <{settings.EMAIL_HOST_USER}>'
            send_mail(
                subject, message,
                email_from, recipient_list,
                fail_silently=False)
        return JsonResponse(data)

    def form_invalid(self, form):
        data = {'success': False, 'errors': form.errors}
        return JsonResponse(data, status=400)


class AddReviewProductView(ReviewMixin, FormView):
    success_url = ''
    form_class = ReviewProductForm

    def form_valid(self, form):
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, pk=product_id)
        if self.request.POST.get('privacy_policy') != 'on':
            return JsonResponse({
                'success': False,
                'errors': {'privacy_policy': [
                    'Подтвердите согласие с политикой безопасности']}},
                    status=400)
        review = form.save(commit=False)
        review.user = self.request.user
        review.product = product
        review.save()
        data = {'success': True}
        config = Config.objects.first()
        recipient_list = [config.email]
        if recipient_list:
            subject = 'Смайк - Новый отзыв добавлен'
            username = self.request.POST.get('username', '')
            message = f'Новый отзыв был добавлен на сайте пользователем {username}.'
            email_from = f'Cайт - {config.site_name} <{settings.EMAIL_HOST_USER}>'
            send_mail(
                subject, message,
                email_from, recipient_list,
                fail_silently=False)
        return JsonResponse(data)

    def form_invalid(self, form):
        data = {'success': False, 'errors': form.errors}
        return JsonResponse(data, status=400)


@require_GET
def get_full_review(request):
    review_id = request.GET.get('review_id')
    review = get_object_or_404(ReviewProduct, id=review_id)
    data = {
        'created_at': review.created_at.strftime('%d.%m.%Y'),
        'name': review.name,
        'text': review.text
    }
    return JsonResponse({'review': data})


class ReviewsList(
        BaseMixin,
        ReviewMixin,
        ListView):
    model = Review
    context_object_name = 'posts'
    template_name = 'reviews/review_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_enabled=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config_seo = Config_seo.objects.first()
        context['meta_title'] = config_seo.reviews_meta_title
        context['meta_description'] = config_seo.reviews_meta_description
        return context
