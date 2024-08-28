from django.contrib import admin

from .models import Message, Spam


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'created_at')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('created_at',)


@admin.register(Spam)
class SpamAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'created_at')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('created_at',)
