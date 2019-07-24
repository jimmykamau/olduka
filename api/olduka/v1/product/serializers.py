from rest_framework import serializers

import olduka.v1.product.models as product_models
import olduka.v1.product.utils as product_utils


class CategorySerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()

    class Meta:
        model = product_models.Category
        fields = (
            '_id', 'name',
            'description', 'image_url'
        )

    def get__id(self, obj):
        return product_utils.get_object_id_value(obj)


class PriceSerializer(serializers.Serializer):
    price = serializers.FloatField()
    discount = serializers.FloatField()


class ProductImageSerializer(serializers.Serializer):
    image_url = serializers.URLField()


class ItemSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    category = CategorySerializer(many=True)
    images = ProductImageSerializer(many=True)
    price = PriceSerializer()

    class Meta:
        model = product_models.Item
        fields = (
            '_id', 'category', 'name',
            'description', 'images', 'price'
        )

    def get__id(self, obj):
        return product_utils.get_object_id_value(obj)
