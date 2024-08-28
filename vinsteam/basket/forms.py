from datetime import datetime

from basket.models import Order
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from users.models import Address

User = get_user_model()


class BaseUserOrderForm(forms.Form):
    phone = PhoneNumberField(
        label="Телефон",
        strip=False,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваш телефон'}),
    )
    first_name = forms.CharField(
        label="Имя",
        strip=False,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваше имя'}),
    )
    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'Введите ваш email'}),
    )
    address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        label='Выберите адрес',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    time_range = forms.ChoiceField(
        choices=Order.TIME_RANGE_CHOICES,
        label='Временной диапазон',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    delivery_date = forms.DateField(
        label='Дата доставки',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.now().strftime('%Y-%m-%d'),
    )
    comment = forms.CharField(
        label="Комментарий",
        strip=False,
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': 'Введите ваше сообщение',
                   'class': 'form_control'}),
    )

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data['delivery_date']
        today = datetime.now().date()

        if delivery_date < today:
            raise ValidationError('Дата доставки не может быть в прошлом.')

        return delivery_date


class UserOrderForm(BaseUserOrderForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            if user.phone:
                self.fields['phone'].initial = user.phone
            if user.email:
                self.fields['email'].initial = user.email
            if user.first_name:
                self.fields['first_name'].initial = user.first_name
            user_addresses = Address.objects.filter(user=user)
            self.fields['address'].queryset = user_addresses
            self.fields['address'].initial = user_addresses[0] if user_addresses else None


class UserOrderAcceptForm(BaseUserOrderForm):
    def __init__(self, *args, addresses=None, **kwargs):
        super().__init__(*args, **kwargs)
        if addresses is not None:
            self.fields['address'].queryset = Address.objects.filter(
                id__in=[addr['id'] for addr in addresses])
