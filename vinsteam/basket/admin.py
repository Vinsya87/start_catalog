from django import forms
from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import BasketProduct, Order, OrderItem


class BasketProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    list_filter = ('user',)


admin.site.register(BasketProduct, BasketProductAdmin)


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'address' in self.fields and self.instance and self.instance.user:
            self.fields[
                'address'].queryset = self.instance.user.addresses.all()


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'city_price']


class CityFilter(admin.SimpleListFilter):
    title = ('Город')
    parameter_name = 'city'

    def lookups(self, request, model_admin):
        cities = Order.objects.exclude(
            address__isnull=True).values_list(
                'address__city__id', 'address__city__name').distinct()
        return cities

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(address__city__id=self.value())
        return queryset


@admin.register(Order)
class OrderAdmin(VersionAdmin):
    form = OrderAdminForm
    list_display = [
        'id',
        'name',
        'get_city',
        'phone',
        'email',
        'status',
        'created_at']
    list_filter = ['status', CityFilter,]
    search_fields = ['name', 'phone', 'email']
    inlines = [OrderItemInline]

    def get_city(self, obj):
        return obj.address.city if obj.address else None

    get_city.short_description = 'Город'

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return [field.name for field in self.opts.local_fields if field.name != 'status']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product']
    list_filter = ['order']
    search_fields = ['order__name', 'product__name']
