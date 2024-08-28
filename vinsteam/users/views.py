from basket.models import BasketProduct
from catalog.models import FavoriteProduct, Product
from django.contrib.auth import (authenticate, get_user_model, login,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import (LogoutView, PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.core.cache import cache
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.generic.edit import DeleteView, UpdateView
from main.views import BaseMixin
from users.forms import (AddressForm, CustomPasswordChangeForm,
                         UserRegistrationForm, UserUpdateForm)
from users.models import Address

User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            user = authenticate(request, email=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse(
                {'success': False, 'message': 'Неверный логин или пароль.'})
    else:
        csrf_token = get_token(request)
        return render(request, 'users/login.html', {'csrf_token': csrf_token})



def is_user_unique(username, email, phone):
    """Проверка уникальности логина, почты и телефона"""

    if User.objects.filter(username=username).exists():
        return False, 'Пользователь с таким именем уже существует.'
    if User.objects.filter(email=email).exists():
        return False, 'Пользователь с такой почтой уже существует.'
    if User.objects.filter(phone=phone).exists():
        return False, 'Пользователь с таким телефоном уже существует.'
    return True, None


def create_user(
        username,
        first_name,
        last_name,
        email,
        phone,
        password,
        session_key,
        favorites,
        basket_products
        ):
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        password=password
    )

    if favorites:
        for product in favorites:
            FavoriteProduct.objects.create(user=user, product=product)
        cache.delete(f'favorites:{session_key}')

    if basket_products:
        for product in basket_products:
            BasketProduct.objects.create(user=user, product=product)
        cache.delete(f'baskets:{session_key}')

    return user


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data['username']
            first_name = cleaned_data['first_name']
            last_name = cleaned_data['last_name']
            email = cleaned_data['email']
            phone = cleaned_data['phone']
            phone = str(phone)
            password = cleaned_data['password']
            password_repeat = cleaned_data['password_repeat']
            if password != password_repeat:
                return JsonResponse({
                    'success': False,
                    'message': 'Пароли не совпадают'})
            if not phone:
                return JsonResponse({
                    'success': False,
                    'message': 'Введите номер телефона'})

            try:
                # Доп валидация
                is_unique, error_message = is_user_unique(
                    username, email, phone)
                if is_unique:
                    session_key = request.session.session_key
                    favorites = cache.get(f'favorites:{session_key}')
                    favorites = Product.objects.filter(
                        pk__in=favorites) if favorites else None
                    baskets = cache.get(f'baskets:{session_key}')
                    basket_products = Product.objects.filter(
                        pk__in=baskets) if baskets else None
                    user = create_user(
                        username,
                        first_name,
                        last_name,
                        email,
                        phone,
                        password,
                        session_key,
                        favorites,
                        basket_products
                    )
                    login(request, user)
                    if user.is_active:
                        return JsonResponse({'success': True})
                    else:
                        return JsonResponse({
                            'success': True,
                            'activation_required': True})
                else:
                    return JsonResponse({
                        'success': False,
                        'message': error_message})
            except Exception as e:
                return JsonResponse(
                    {
                        'success': False,
                        'message': (
                            'Ошибка при создании пользователя. '
                            'Попробуйте еще раз позже. '
                            'Ошибка: {}'.format(str(e))
                        )
                    }
                )
        else:
            error_messages = '<br>'.join(
                [
                    error
                    for error_list in form.errors.values()
                    for error in error_list
                ]
            )
            return JsonResponse(
                {'success': False,
                 'message': f'{error_messages}'})
    else:
        return JsonResponse({
            'success': False,
            'message': 'Метод запроса должен быть POST.'})


@method_decorator(login_required, name='dispatch')
class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': ['Logout error']})


class UserDetailsView(
        BaseMixin,
        FormView):
    template_name = 'users/profile.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs['instance'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Профиль'
        return context

    def form_valid(self, form):
        form.save()
        password_form = PasswordChangeForm(
            user=self.request.user,
            data=self.request.POST)
        if password_form.is_valid():
            password_form.save()
        return super().form_valid(form)


class PasswordChangeView(
        BaseMixin,
        FormView):
    template_name = 'users/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Смена пароля'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)


class CustomResetView(PasswordResetView, BaseMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return super(BaseMixin, self).get_context_data(**context)


class CustomResetDoneView(PasswordResetDoneView, BaseMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return super(BaseMixin, self).get_context_data(**context)


class CustomResetCompleteView(PasswordResetCompleteView, BaseMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return super(BaseMixin, self).get_context_data(**context)


class CustomResetConfirmView(PasswordResetConfirmView, BaseMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return super(BaseMixin, self).get_context_data(**context)


class AddressFormView(
        BaseMixin,
        FormView):
    template_name = 'users/address_form.html'
    form_class = AddressForm
    success_url = reverse_lazy('users:add_address')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            addresses = Address.objects.filter(user=self.request.user)
            context['addresses'] = addresses
        context['page_name'] = 'Адреса доставки'
        return context

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user
        address.save()
        return redirect('users:add_address')


class AddressEditView(
        BaseMixin,
        UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'users/address_edit.html'
    success_url = reverse_lazy('users:add_address')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Редактировать адрес'
        return context

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user
        address.save()
        return redirect('users:add_address')


class AddressDeleteView(
        DeleteView):
    model = Address
    template_name = 'users/address_delete.html'
    success_url = reverse_lazy('users:add_address')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
