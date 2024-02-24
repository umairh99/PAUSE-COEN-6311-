# registration_app/serializers.py

from rest_framework import serializers
from .models import User,Agent

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