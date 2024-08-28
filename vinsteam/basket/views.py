import json

from asgiref.sync import sync_to_async
from basket.forms import UserOrderAcceptForm, UserOrderForm
from basket.models import BasketProduct, Order, OrderItem
from catalog.models import Product
from config_site.models import Config, Config_seo
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import aget_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from django.views.generic import ListView, TemplateView
from django.views.generic.base import View
from main.views import BaseMixin, check_user_authenticated
from users.models import Address, User


class AddToBasketView(View):
    """Общее добавление в корзину"""
    http_method_names = ['post']

    async def post(self, request, pk):
        product = await aget_object_or_404(Product, pk=pk)
        session_key = request.session.session_key

        if await check_user_authenticated(request):
            try:
                basket_product = await sync_to_async(
                    BasketProduct.objects.get)(
                    user=request.user, product=product)
                await sync_to_async(basket_product.delete)()
                added = False
            except BasketProduct.DoesNotExist:
                basket_product = await BasketProduct.objects.acreate(
                    user=request.user, product=product)
                added = True
        else:
            baskets = await cache.aget(f'baskets:{session_key}')
            if not baskets:
                baskets = {}
            else:
                baskets = dict(baskets)
            if pk not in baskets:
                baskets[pk] = 1
                await cache.aset(f'baskets:{session_key}', baskets)
                added = True
            else:
                del baskets[pk]
                await cache.aset(f'baskets:{session_key}', baskets)
                added = False

        return JsonResponse({'added': added})


@require_POST
async def update_basket_quantity(request, product_id):
    data = json.loads(request.body.decode('utf-8'))
    new_quantity = max(1, int(data.get('new_quantity', 0)))
    if await check_user_authenticated(request):
        try:
            basket_product = await BasketProduct.objects.aget(
                user=request.user, product_id=product_id)
            created = False
        except BasketProduct.DoesNotExist:
            basket_product = BasketProduct(
                user=request.user,
                product_id=product_id,
                quantity=new_quantity)
            created = True
    else:
        session_key = request.session.session_key
        baskets = await cache.aget(f'baskets:{session_key}')
        if not baskets:
            baskets = {}
        else:
            baskets = dict(baskets)
        if product_id in baskets:
            baskets[product_id] = new_quantity
            await cache.aset(f'baskets:{session_key}', baskets)
            created = True
        else:
            del baskets[product_id]
            await cache.aset(f'baskets:{session_key}', baskets)
            created = False

        return JsonResponse({
            'success': True,
            'new_quantity': new_quantity,
            'created': True})
    basket_product.quantity = new_quantity
    await basket_product.asave()

    return JsonResponse({
        'success': True,
        'new_quantity': basket_product.quantity,
        'created': created})


class BasketView(
        BaseMixin,
        ListView):
    template_name = 'order/basket.html'
    model = BasketProduct
    context_object_name = 'baskets'

    def add_basket_info_to_context(self, context, product):
        quantity = 1
        if self.request.user.is_authenticated:
            try:
                basket_product = BasketProduct.objects.get(
                    user=self.request.user, product=product)
                quantity = basket_product.quantity
            except BasketProduct.DoesNotExist:
                pass
        else:
            session_key = self.request.session.session_key
            baskets = cache.get(f'baskets:{session_key}')
            if baskets:
                quantity = baskets.get(product.pk, 1)
        return quantity

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return BasketProduct.objects.filter(user=self.request.user)
        else:
            session_key = self.request.session.session_key
            baskets = cache.get(f'baskets:{session_key}', set())
            basket_products = Product.objects.filter(pk__in=baskets)
            return [
                BasketProduct(product=prod)
                for prod in basket_products]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Корзина'
        context['meta_title'] = 'Корзина'
        context['meta_description'] = 'Корзина с продукцией.'
        context['products_with_prices'] = context['baskets']
        for product_with_price in context['products_with_prices']:
            quantity = self.add_basket_info_to_context(
                context, product_with_price.product)
            product_with_price.quantity = quantity

        return context


def send_order_confirmation_email(order, request):
    admin_order_change_url = reverse('admin:%s_%s_change' % (
        Order._meta.app_label, Order._meta.model_name), args=[order.id])
    order_admin_link = (
        f'{request.scheme}://{request.get_host()}'
        f'{admin_order_change_url}'
    )
    html_message = render_to_string('mail/order_mail.html', {
        'order': order,
        'order_admin_link': order_admin_link})
    subject = f'Новый заказ №{order.id}'
    email_from = f'Смайк - сайт <{settings.EMAIL_HOST_USER}>'
    config = Config.objects.first()
    admin_email = config.email
    recipient_list = [admin_email]
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        email_from,
        recipient_list,
        html_message=html_message,
        fail_silently=False)


def send_order_confirmation_user(order, request):
    html_message = render_to_string(
        'mail/order_mail_user.html', {'order': order})
    config = Config.objects.first()
    subject = f'Ваш заказ {config.site_name}'
    email_from = f'Смайк - сайт <{settings.EMAIL_HOST_USER}>'
    recipient_list = [order.email]
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        email_from,
        recipient_list,
        html_message=html_message,
        fail_silently=False)


class OrderView(BaseMixin, TemplateView):
    template_name = 'order/order.html'
    model = BasketProduct
    context_object_name = 'baskets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Оформление заказа'
        context['baskets'] = self.get_baskets()
        context['products_with_prices'] = []
        config_seo = Config_seo.objects.first()
        context['meta_title'] = config_seo.basket_meta_title
        context['meta_description'] = config_seo.basket_meta_description
        context['form'] = self.get_form()

        if self.request.user.is_authenticated:
            for product_with_price in context['baskets']:
                quantity = self.add_basket_info_to_context(
                    context,
                    product_with_price.product)
                product_with_price.quantity = quantity
                if product_with_price.product.get_price_for_city() is not None:
                    context['products_with_prices'].append(product_with_price)
                    context['order_true'] = True
        return context

    def add_basket_info_to_context(self, context, product):
        quantity = 1
        if self.request.user.is_authenticated:
            try:
                basket_product = BasketProduct.objects.get(
                    user=self.request.user, product=product)
                quantity = basket_product.quantity
            except BasketProduct.DoesNotExist:
                pass
        else:
            session_key = self.request.session.session_key
            baskets = cache.get(f'baskets:{session_key}')
            if baskets:
                quantity = baskets.get(product.pk, 1)
        return quantity

    def get_baskets(self):
        if self.request.user.is_authenticated:
            return BasketProduct.objects.filter(user=self.request.user)
        return []

    # Метод для создания формы
    def get_form(self):
        form_kwargs = self.get_form_kwargs()
        return UserOrderForm(**form_kwargs)

    # Метод для передачи параметров в форму
    def get_form_kwargs(self):
        kwargs = {}
        if self.request.user.is_authenticated:
            kwargs['user'] = self.request.user
            kwargs['initial'] = {
                'phone': self.request.user.phone,
                'email': self.request.user.email,
                'first_name': self.request.user.first_name,
            }
        return kwargs


@sync_to_async
def check_user(request):
    return request.user.id


class AsyncOrderSubmitView(View):
    """Асинхронная обработка отправки заказа."""
    http_method_names = ['post']

    async def post(self, request):
        user_id = await check_user(request)
        user = await User.objects.aget(id=user_id)
        user_addresses = []
        async for address in Address.objects.filter(user=user):
            user_addresses.append({
                'id': address.id,
                'name': address.name
            })

        form = UserOrderAcceptForm(request.POST, addresses=user_addresses)

        if not await sync_to_async(form.is_valid)():
            return JsonResponse({
                'success': False,
                'errors': form.errors.as_json()})
        baskets = await self.get_baskets(request)
        if not baskets:
            return JsonResponse({
                'success': False,
                'message': 'Корзина пуста.'})

        order = await Order.objects.acreate(
            user=user,
            name=form.cleaned_data['first_name'],
            phone=form.cleaned_data['phone'],
            email=form.cleaned_data['email'],
            address=form.cleaned_data['address'],
            time_range=form.cleaned_data['time_range'],
            delivery_date=form.cleaned_data['delivery_date'],
            message=form.cleaned_data['comment']
        )
        order_items = []
        total_price = 0
        for basket in baskets:
            async for basket in BasketProduct.objects.select_related(
                    'product').filter(user_id=user_id):
                product_price = basket.product.price
                if product_price:
                    order_item = await OrderItem.objects.acreate(
                        order=order,
                        product=basket.product,
                        quantity=basket.quantity,
                        city_price=product_price
                    )
                    order_items.append(order_item)
                    product = basket.product
                    product.counter += 1
                    await product.asave()
                    basket = await BasketProduct.objects.aget(id=basket.id)
                    await basket.adelete()
                    total_price += basket.quantity * product_price
        order.total_price = total_price
        await order.asave()

        return JsonResponse({'success': True, 'order_id': order.id})

    async def get_baskets(self, request):
        if await check_user_authenticated(request):
            user_id = request.user.id

            # Асинхронный фильтр корзин по пользователю
            baskets = []
            async for basket in BasketProduct.objects.filter(user_id=user_id):
                baskets.append(basket)

            return baskets
        return []


class UserOrderListView(
        BaseMixin,
        LoginRequiredMixin,
        ListView):
    model = Order
    template_name = 'order/user_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Заказы'
        return context
