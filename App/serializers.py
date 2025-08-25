from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    available_units = serializers.IntegerField(source='stock', read_only=True)
    price = serializers.FloatField()
    rating = serializers.FloatField()

    class Meta:
        model = Product
        fields = ['id','name','description','category','brand','price','rating','available_units']

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
