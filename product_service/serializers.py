from rest_framework import serializers
from .models import Category, Product, Book, Phone, Clothing

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 
                  'category', 'category_name', 'image', 'created_at']

class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'price', 'stock', 
                  'category', 'category_name', 'image', 'created_at',
                  'author', 'isbn', 'publisher', 'pages']

class PhoneSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Phone
        fields = ['id', 'name', 'description', 'price', 'stock', 
                  'category', 'category_name', 'image', 'created_at',
                  'brand', 'model_name', 'screen_size', 'memory', 'storage']

class ClothingSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Clothing
        fields = ['id', 'name', 'description', 'price', 'stock', 
                  'category', 'category_name', 'image', 'created_at',
                  'brand', 'size', 'color', 'material', 'gender']