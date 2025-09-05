from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Product, Category, Cart, Review, Order

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','name']

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    rating = serializers.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0.0)
    category = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True)

    class Meta:
        model = Product
        fields = ['id','name','description','category','category_id','brand','price','rating','stock']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    product = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Cart
        fields = ['user','product','quantity']

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)

    rating = serializers.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Review
        fields = ['user_id','product_id','username','product_name','rating','review','created_at','updated_at']
    
class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    total_amount = serializers.FloatField()
    units = serializers.IntegerField()

    user_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['user_id','product_id','username','product','units','total_amount','status','created_at']