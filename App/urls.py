from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.ListUsers.as_view()),
    path('register/', views.UserRegistration.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('products/all/', views.ListProducts.as_view()),
    path('products/<int:id>', views.ListSingleProduct),
    path('products/create/', views.CreateProduct),
]
