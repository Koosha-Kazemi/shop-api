from rest_framework import serializers

from .models import Category, Product,ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'final_price_value')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ('is_active','index')
      


class ProductDetailSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer(source='product_images', many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
      
        


