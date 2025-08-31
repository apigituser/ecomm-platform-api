from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistration.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    path('users/', views.ListUsers.as_view()),
    path('users/delete/', views.DeleteUser),
    
    path('products/', views.ListCreateProduct),
    path('products/<int:id>', views.ListUpdateDeleteProduct),
    
    path('cart/', views.ListCreateCartItem),
    path('cart/<int:product_id>', views.UpdateDeleteCartItem),
    
    path('category/', views.BulkAddCategory),
    path('category/<int:id>', views.DeleteCategory),

    path('review/', views.ListReviews),
]
