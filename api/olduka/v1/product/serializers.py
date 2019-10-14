from rest_framework import serializers

import olduka.v1.product.models as product_models
import olduka.v1.serializers as base_serializers
import olduka.v1.utils as base_utils


class CategorySerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    subcategory = base_serializers.RecursiveField(many=True)

    class Meta:
        model = product_models.Category
        fields = (
            '_id', 'name',
            'description', 'image_url', 'subcategory'
        )

    def get__id(self, obj):
        return base_utils.get_object_id_value(obj)


class PriceSerializer(serializers.Serializer):
    price = serializers.FloatField()
    discount = serializers.FloatField()


class ProductImageSerializer(serializers.Serializer):
    image_url = serializers.URLField()


class ItemSerializer(base_serializers.DynamicFieldsModelSerializer):
    _id = serializers.CharField()
    category = CategorySerializer(many=True, required=False)
    images = ProductImageSerializer(many=True, required=False)
    price = PriceSerializer(required=False)

    class Meta:
        model = product_models.Item
        fields = (
            '_id', 'category', 'name', 'quantity',
            'description', 'images', 'price'
        )


class CategoryItemSerializer(serializers.ModelSerializer):
    category_item = ItemSerializer(many=True)

    class Meta:
        model = product_models.Category
        fields = ('name', 'description', 'image_url', 'category_item')
