from django.urls import path
from . import views
from .views import UserProfileView, RegisterView
from .views import CustomTokenObtainPairView
from .views import UserDetailView


urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/user/<int:user_id>/', views.UserProfileView.as_view(), name='user-profile'),
]

