from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def days_until(piggybank_date):
    current_date = timezone.now().date()
    days_remaining = (piggybank_date - current_date).days
    return days_remaining
