from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile
import re

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role']

def validate_username(value):
    # Allow letters, numbers, spaces, dashes, and underscores
    if not re.match(r'^[\w\s-]+$', value):
        raise serializers.ValidationError("Username can only contain letters, numbers, spaces, dashes, and underscores.")
    return value



class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[validate_username])
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        UserProfile.objects.create(user=user, role=role)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']