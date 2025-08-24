from django.contrib import admin
from .models import UserReview, Category, Product, Order

admin.site.register(UserReview)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
