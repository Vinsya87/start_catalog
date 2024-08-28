from django.contrib import admin
from django.utils.html import format_html

from .models import City, Config, Config_seo


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'address', 'email', 'phone_number', 'logo']

@admin.register(Config_seo)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['title',]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']