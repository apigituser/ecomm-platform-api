from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.ListUsers.as_view()),
    path('register/', views.UserRegistration.as_view()),
    path('login/', TokenObtainPairView.as_view()),
]
