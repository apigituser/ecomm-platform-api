from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Product, Category, Cart, Review

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','name','count']

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    rating = serializers.FloatField()
    
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_id = serializers.IntegerField(source="category.id", write_only=True)

    class Meta:
        model = Product
        fields = ['id','name','description','category_id','category_name','brand','price','rating','stock']

    def create(self, validated_data):
        category_id = validated_data.pop('category').get('id')
        item = get_object_or_404(Category, id=category_id)
        item.count += 1
        item.save()
        validated_data['category'] = item
        product = Product.objects.create(**validated_data)
        return product

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
    user = serializers.CharField(source="user.username")
    product = ProductSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Review
        fields = '__all__'
