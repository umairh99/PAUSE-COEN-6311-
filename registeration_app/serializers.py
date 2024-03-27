# registration_app/serializers.py

from rest_framework import serializers
from .models import User,Agent,Hotel, Flight, View, TravelPackage, PackageItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'date_of_birth', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Ensures password is write-only in responses

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent  # Replace Agent with your actual model name
        fields = ['id', 'name', 'email', 'phone', 'date_of_birth', 'password', 'agency_name']
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only in responses

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = '__all__'

class TravelPackageSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = TravelPackage
        fields = '__all__'

    def get_items(self, obj):
        items = PackageItem.objects.filter(package=obj)
        return PackageItemSerializer(items, many=True).data

class PackageItemSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()
    flight = FlightSerializer()
    view = ViewSerializer()

    class Meta:
        model = PackageItem
        fields = '__all__'