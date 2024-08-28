from bs4 import BeautifulSoup
from django import template

register = template.Library()

@register.filter
def clean_html(value):
    if value is None:
        return ''
    soup = BeautifulSoup(value, 'html.parser')
    for tag in soup.find_all():
        if not tag.get_text(strip=True):
            tag.extract()
    return str(soup)
