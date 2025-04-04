from rest_framework import serializers

from .models import (Category,
                      Product,
                      ProductImage,
                      OptionGroup,
                      OptionValue,
                      )


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
        exclude = ('index',)
      


class ProductDetailSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer(source='product_images', many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance:Product):
        data = super().to_representation(instance)
        categories = instance.category.all()
        data['category'] = [category.title for category in categories]

        return data
    



class OptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionValue
        fields = '__all__'



class OptionAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionValue
        fields = '__all__'

    


