from articles.models import MenuItem
from django.views.generic.base import ContextMixin


class MenuView(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_menu_items = MenuItem.objects.filter(
            is_active=True).order_by('order')
        context['main_menu_items'] = active_menu_items.filter(
            is_main_menu=True)
        context['mobile_menu_items'] = active_menu_items.filter(
            is_mobile_menu=True)
        context['footer_menu_items'] = active_menu_items.filter(
            is_footer_menu=True)
        context['other_menu_items'] = active_menu_items.filter(
            is_other_menu=True)

        return context
