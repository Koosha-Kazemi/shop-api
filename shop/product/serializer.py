from rest_framework import serializers

from .models import Category, Product,ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)
        read_only_fields = ('index',)


class ProductSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('final_price_value',)

        


