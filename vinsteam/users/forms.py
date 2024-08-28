from config_site.models import City
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from users.models import Address

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form_control',
            'placeholder': 'Повторите пароль'})
    )
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'form_control',
            'placeholder': 'Телефон*',
            'required': True,
            'autocomplete': 'phone'})
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'password']
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'form_control',
                'placeholder': 'Пароль*',
                'autocomplete': 'new-password'}),
            'username': forms.TextInput(attrs={
                'class': 'form_control',
                'placeholder': 'Логин*',
                'required': True}),
            'first_name': forms.TextInput(attrs={
                'class': 'form_control',
                'placeholder': 'Ваше имя*',
                'required': True,
                'autocomplete': 'first_name'}),
            'last_name': forms.TextInput(attrs={
                'class': 'form_control',
                'placeholder': 'Ваша фамилия',
                'autocomplete': 'last_name'}),
            'email': forms.EmailInput(attrs={
                'class': 'form_control',
                'placeholder': 'E-mail*',
                'autocomplete': 'email',
                'id': 'id_email_2'}),
        }


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'groups',
            'user_permissions')
        widgets = {
            'groups': forms.CheckboxSelectMultiple,
            'user_permissions': FilteredSelectMultiple(
                'Разрешения',
                is_stacked=False),
        }


class AdminUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'groups')
        widgets = {
            'groups': forms.CheckboxSelectMultiple,
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите ваш email'}),
    )
    phone = forms.CharField(
        label="Телефон",
        strip=False,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваш телефон',
            'id': 'id_phone_3'}),
    )
    first_name = forms.CharField(
        label="Имя",
        strip=False,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваше имя'}),
    )
    last_name = forms.CharField(
        label="Фамилия",
        strip=False,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите вашу фамилию',
            'id': 'id_last_3'}),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            if user.email:
                self.fields['email'].initial = user.email
            if user.phone:
                self.fields['phone'].initial = user.phone
            if user.first_name:
                self.fields['first_name'].initial = user.first_name
            if user.last_name:
                self.fields['last_name'].initial = user.last_name

    class Meta:
        model = User
        fields = [
                    'email',
                    'phone',
                    'first_name',
                    'last_name']


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Введите старый пароль'}),
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Введите новый пароль'}),
    )
    new_password2 = forms.CharField(
        label="Подтвердите пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Подтвердите пароль'}),
    )


class AddressForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        label='Город', empty_label='Выберите город',
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}))

    name = forms.CharField(
        label="Название адреса",
        strip=False,
        widget=forms.TextInput(attrs={'placeholder': 'Название'}),
    )
    street = forms.CharField(
        label="Улица",
        strip=False,
        widget=forms.TextInput(attrs={'placeholder': 'Улица'}),
    )
    building = forms.CharField(
        label="Дом",
        strip=False,
        widget=forms.TextInput(attrs={'placeholder': 'Дом'}),
    )
    apartment = forms.CharField(
        label="Квартира/офис",
        strip=False,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Квартира/офис'}),
    )

    class Meta:
        model = Address
        fields = ['name', 'city', 'street', 'building', 'apartment']
