from config_site.models import Config
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.base import ContextMixin
from mail_post.forms import ContactForm
from mail_post.models import Message, Spam
from phonenumber_field.formfields import PhoneNumberField


class FeedView(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_feed'] = ContactForm()
        return context


class SendEmailView(View):

    def post(self, request):
        form = ContactForm(request.POST)
        tel = request.POST.get('phone_number', '')
        form.full_clean()
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            tel = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']
            # Проверяем введенное имя на наличие цифр и специальных символов
            if not name.replace(' ', '').isalpha():
                # Если имя содержит неподходящие символы, возвращаем сообщение об ошибке в JSON-ответе
                return JsonResponse({'errors': 'Имя не должно содержать цифр или специальных символов.'}, status=400)
            # Создаем экземпляр модели Message и сохраняем его
            message_obj = Message(name=name, email=email, phone_number=tel, message=message)
            message_obj.save()
            message_id = message_obj.id
            # Формируем текст сообщения
            if not email:
                message_text = f'Номер: {message_id}\n' \
                               f'Имя: {name}\n' \
                               f'Телефон: {tel}\n' \
                               f'Сообщение: {message}\n'
            else:
                message_text = f'Номер: {message_id}\n' \
                               f'Имя: {name}\n' \
                               f'E-mail: {email}\n' \
                               f'Телефон: {tel}\n' \
                               f'Сообщение: {message}\n'
            # Отправляем сообщение по почте
            email_from = f'Общее сообщение - №{message_id} с сайта - <{settings.EMAIL_HOST_USER}>'
            subject = 'Письмо'
            try:
                config = Config.objects.first()
                recipient_list = [config.email]
                if recipient_list:
                    send_mail(
                        subject, message_text,
                        email_from, recipient_list,
                        fail_silently=False)
                    # Возвращаем успешный ответ в формате JSON
                    return JsonResponse({'success': 'Сообщение успешно отправлено'}, status=200)
                else:
                    return JsonResponse({'error': 'Список получателей не задан.'}, status=400)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Не удалось получить список получателей из базы данных.'}, status=500)
        else:
            spam_obj = Spam(name=request.POST.get('name', ''), email=request.POST.get('email', ''),
                            phone_number=tel, message=request.POST.get('message', ''))
            spam_obj.save()
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = [str(error) for error in error_list]
            return JsonResponse({'errors': errors}, status=400)


def send_email_view(request):
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        name = request.POST.get('username', '')
        email = request.POST.get('email', '')
        tel = request.POST.get('tel', '')
        message = request.POST.get('message', '')
        # Проверяем введенное имя на наличие цифр и специальных символов
        if not name.replace(' ', '').isalpha():
            # Если имя содержит неподходящие символы, возвращаем сообщение об ошибке в JSON-ответе
            return JsonResponse({'error': 'Имя не должно содержать цифр или специальных символов.'}, status=400)

        try:
            phone_number = PhoneNumberField().clean(tel)
        except ValidationError:
            # Если номер телефона неправильный, возвращаем сообщение об ошибке в JSON-ответе
            return JsonResponse({'error': 'Неправильный номер телефона.'}, status=400)

        # Создаем экземпляр модели Message и сохраняем его
        message = Message(name=name, email=email, phone_number=phone_number, message=message)
        message.save()

        # Формируем текст сообщения
        if not email:
            message_text = f'Имя: {name}\n' \
                      f'Телефон: {tel}\n' \
                      f'Сообщение: {message.message}\n'
        else:
            message_text = f'Имя: {name}\n' \
                      f'E-mail: {email}\n' \
                      f'Телефон: {tel}\n' \
                      f'Сообщение: {message.message}\n'

        # Отправляем сообщение по почте
        email_from = f'Общее сообщение с сайта - <{settings.EMAIL_HOST_USER}>'
        subject = 'Письмо'

        try:
            config = Config.objects.first()
            recipient_list = [config.email]
            if recipient_list:
                send_mail(
                    subject, message_text,
                    email_from, recipient_list,
                    fail_silently=False)
                # Возвращаем успешный ответ в формате JSON
                return JsonResponse({'success': 'Сообщение успешно отправлено'}, status=200)
            else:
                return JsonResponse({'error': 'Список получателей не задан.'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Не удалось получить список получателей из базы данных.'}, status=500)
    return render(request, 'send_email.html')
