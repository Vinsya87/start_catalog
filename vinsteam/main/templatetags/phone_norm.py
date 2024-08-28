from django import template

register = template.Library()

@register.filter
def format_phone_number(phone_number):
    phone_number = ''.join(filter(str.isdigit, phone_number))
    if not phone_number.startswith('+7'):
        phone_number = '+7' + phone_number[1:]

    return phone_number
