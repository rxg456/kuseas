from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'password', 'is_superuser', 'username',
            'email', 'is_active', 'phone'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'default': False},
            'is_active': {'default': False},
            'username': {'min_length': 3, 'max_length': 16}
        }

    def validate_password(self, value):
        if 4 <= len(value) <= 16:
            # encrypt
            return make_password(value)
        raise serializers.ValidationError('The length of password must be between 4 and 16.')
