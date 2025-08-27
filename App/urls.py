from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.ListUsers.as_view()),
    path('users/delete/', views.DeleteUser),
    path('register/', views.UserRegistration.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('products/all/', views.ListProducts.as_view()),
    path('products/<int:id>', views.ListSingleProduct),
    path('products/create/', views.CreateProduct),
    path('products/update/<int:id>', views.UpdateProduct),
    path('products/delete/<int:id>', views.DeleteProduct),
    path('cart/', views.ListCartItems),
]
