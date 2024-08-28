from django.urls import path

from .views import SendEmailView, send_email_view

app_name = 'mail_post'

urlpatterns = [
    path('send_email/', send_email_view, name='send_email'),
    path('send_email_two/', SendEmailView.as_view(), name='send_email_two'),
    ]
