from rest_framework import serializers


class CreatePaymentSerializer(serializers.Serializer):
    value = serializers.DecimalField(max_digits=10, decimal_places=2)
