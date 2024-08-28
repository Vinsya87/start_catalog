import json

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import CreatePaymentSerializer
from .services.create_payment import create_payment
from .services.payment_acceptance import payment_acceptance


class CreatePaymentView(CreateAPIView):
    template = 'moneybox/balance.html'
    serializer_class = CreatePaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreatePaymentSerializer(data=request.POST)
        if serializer.is_valid():
            serialized_data = serializer.validated_data
            user = request.user
            serialized_data['user_id'] = user.id
            return_url = reverse('moneybox:balance')
            current_site = get_current_site(request)
            full_return_url = f"http://{current_site.domain}{return_url}"
            serialized_data['return_url'] = full_return_url
            confirmation_url = create_payment(serialized_data)
            return HttpResponseRedirect(confirmation_url)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class CreatePaymentAcceptanceView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        response = json.loads(request.body)
        if payment_acceptance(response):
            return Response(200)
        return Response(404)
