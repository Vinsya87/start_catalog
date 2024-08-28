from django.contrib import admin

from .models import Review, ReviewProduct


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'is_enabled')
    list_filter = ('is_enabled',)
    list_editable = ('is_enabled',)


admin.site.register(Review, ReviewAdmin)


class ReviewProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'is_enabled')
    list_filter = ('is_enabled',)
    list_editable = ('is_enabled',)


admin.site.register(ReviewProduct, ReviewProductAdmin)
