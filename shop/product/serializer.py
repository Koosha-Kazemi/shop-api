from rest_framework import serializers

from .models import Category, Product, Image, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('final_price_value',)

        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


