from basket.views import (AddToBasketView, AsyncOrderSubmitView, BasketView,
                          OrderView, UserOrderListView, update_basket_quantity)
from django.urls import path

app_name = 'basket'

urlpatterns = [
    path(
        'add-to-basket/<int:pk>/',
        AddToBasketView.as_view(),
        name='add_to_basket'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('order/', OrderView.as_view(), name='order'),
    path('order/submit/', AsyncOrderSubmitView.as_view(), name='order_submit'),
    path('orders/', UserOrderListView.as_view(), name='orders_users'),
    path('update-basket-quantity/<int:product_id>/',
         update_basket_quantity, name='update_basket_quantity'),
]
