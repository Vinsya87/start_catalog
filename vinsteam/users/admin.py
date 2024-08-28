from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

from .forms import CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': (
                'phone',)}),
        )
    form = CustomUserChangeForm
    list_display = ('pk', 'username', 'is_active', 'phone', 'email')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('username', 'is_active')
    list_editable = ('is_active',)
    empty_value_display = '-пусто-'


admin.site.register(User, CustomUserAdmin)
