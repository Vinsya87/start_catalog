from django.apps import AppConfig


class MailPostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mail_post'
    verbose_name = 'Сообщения на почту'
