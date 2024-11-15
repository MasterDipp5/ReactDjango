from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import UserProfile
from .serializers import UserProfileSerializer, RegisterSerializer, UserSerializer

User = get_user_model()  # Using get_user_model for flexibility with custom user models

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Fetch the user profile by user_id
        user_profile = get_object_or_404(UserProfile, user_id=user_id)  # Adjust as needed
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        try:
            # Attempt to fetch UserProfile and add role to token if it exists
            user_profile = UserProfile.objects.get(user=user)
            token['role'] = user_profile.role
        except UserProfile.DoesNotExist:
            token['role'] = None
            print(f"UserProfile does not exist for user {user.username}")
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, *args, **kwargs):
        # Fetch the UserProfile using user_id and serialize the data
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
