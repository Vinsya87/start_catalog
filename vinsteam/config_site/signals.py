from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Config_seo
from .utils import process_favicon


@receiver(post_save, sender=Config_seo)
def handle_favicon_processing(sender, instance, **kwargs):
    if instance.favicon:
        process_favicon(instance)
