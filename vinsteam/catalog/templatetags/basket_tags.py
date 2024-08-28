from django import template

register = template.Library()


@register.simple_tag
def get_basket_product_total_price(product):
    return product.product.price * product.quantity
