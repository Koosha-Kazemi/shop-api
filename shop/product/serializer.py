from rest_framework import serializers

from .models import (Category, OptionAttribute,
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
    main_image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = ('title', 'final_price_value', 'main_image')

    def get_main_image(self, obj:Product):
        try:
            main_image = obj.product_images.get(index=0)
            return ProductImageSerializer(main_image).data
        except ProductImage.DoesNotExist:
            return None
    


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
    


class OptionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionGroup
        fields = '__all__'


class OptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionValue
        fields = '__all__'



class OptionAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionAttribute
        fields = '__all__'
        

