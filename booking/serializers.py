from rest_framework import serializers

from booking.models import Orders, Seat


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'
