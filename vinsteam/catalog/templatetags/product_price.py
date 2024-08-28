from django import template

register = template.Library()


@register.simple_tag
def get_product_price_for_city(product):
    return product.get_price_for_city()
