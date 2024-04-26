from rest_framework import serializers
from .models import User


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_active', 'is_superuser', 'is_staff']
        read_only_fields = ['email', 'last_login', 'is_agent']

    def update(self, instance, validated_data):
        if validated_data.get('picture') and validated_data.get('picture'):
            instance.picture.delete(save=True)
        return super().update(instance, validated_data)


class UpdatePassSerializer(serializers.Serializer):
    currentPass = serializers.CharField()
    newPass = serializers.CharField()
    newPass2 = serializers.CharField()
