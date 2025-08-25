from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    available_units = serializers.IntegerField(source='stock', read_only=True)
    price = serializers.FloatField()
    rating = serializers.FloatField()

    class Meta:
        model = Product
        fields = ['id','name','description','category','brand','price','rating','available_units']
