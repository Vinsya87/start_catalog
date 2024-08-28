from django import forms
from django.core.exceptions import ValidationError

from .models import Review, ReviewProduct


class BaseReviewForm(forms.ModelForm):

    def clean_name(self):
        name = self.cleaned_data['name']
        if not all(char.isalpha() or char.isspace() for char in name):
            raise ValidationError(
                'Имя не должно содержать цифр или специальных символов.')
        return name

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        model = kwargs.pop('model', None)
        super(BaseReviewForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['name'].initial = user.first_name
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = user.phone
        if model:
            self.Meta.model = model

    class Meta:
        fields = ('name', 'email', 'phone', 'text')
        labels = {
            'name': '',
            'email': '',
            'phone': '',
            'text': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form_control',
                'placeholder': 'Имя'}),
            'email': forms.EmailInput(attrs={
                'class': 'form_control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={
                'class': 'form_control',
                'placeholder': 'Телефон', 'id': None}),
            'text': forms.Textarea(attrs={
                'class': 'form_control', 'placeholder': 'Ваш отзыв'}),
        }


class ReviewForm(BaseReviewForm):
    class Meta(BaseReviewForm.Meta):
        model = Review


class ReviewProductForm(BaseReviewForm):
    class Meta(BaseReviewForm.Meta):
        model = ReviewProduct
