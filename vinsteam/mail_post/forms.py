import re

from articles.models import Post
from django import forms
from django.core.exceptions import ValidationError
from mail_post.models import Message


class ContactForm(forms.ModelForm):

    def clean_message(self):
        message = self.cleaned_data['message']
        # Проверка на количество ссылок
        if len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)) > 2:
            raise ValidationError('Сообщение не должно содержать более двух ссылок.')
        # Проверка на длину сообщения
        if len(message) > 800:
            raise ValidationError('Сообщение должно содержать не более 800 символов.')
        return message

    class Meta:
        model = Message
        fields = ['name', 'email', 'phone_number', 'message']
        labels = {
            'name': '',
            'email': '',
            'phone_number': '',
            'message': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Имя', 'id': 'name_field'}),
            'email': forms.EmailInput(attrs={'class': 'form_control', 'placeholder': 'Email', 'id': 'id_pochta'}),
            'phone_number': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Телефон', 'id': 'id_telephon'}),
            'message': forms.Textarea(attrs={'class': 'form_control', 'placeholder': 'Напишите дополнительную информацию *', 'autocomplete': 'off', 'id': 'message_field'}),
        }
