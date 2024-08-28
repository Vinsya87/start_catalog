from django.urls import path
from yookassa_payment.views import (CreatePaymentAcceptanceView,
                                    CreatePaymentView)

app_name = 'yookassa_payment'

urlpatterns = [
    path('create_payment/',
         CreatePaymentView.as_view(),
         name='create_payment'),
    path('payment_acceptance/',
         CreatePaymentAcceptanceView.as_view(),
         name='payment_acceptance'),
]
