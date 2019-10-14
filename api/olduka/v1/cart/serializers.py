from rest_framework import serializers

import olduka.v1.authentication.serializers.user_serializers as user_serializers
import olduka.v1.cart.models as cart_models
import olduka.v1.product.models as product_models
import olduka.v1.product.serializers as product_serializers
import olduka.v1.utils as base_utils
from olduka.v1.cart import logger


class CartItemSerializer(serializers.ModelSerializer):
    item = product_serializers.ItemSerializer()

    class Meta:
        model = cart_models.CartItem
        fields = ('item', 'quantity')
    
    def create(self, validated_data):
        product = validated_data.pop('item', None)
        if product is not None:
            item = product_models.Item.objects.get(_id=product['_id'])
            instance = cart_models.CartItem.objects.create(
                item=item, quantity=validated_data['quantity'])
            return instance
        raise serializers.ValidationError(
            "An item with the id provided doesn't exist"
        )


class CartSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    user = user_serializers.UserSerializer(required=False)
    items = CartItemSerializer(many=True, required=False)

    class Meta:
        model = cart_models.Cart
        fields = ('_id', 'user', 'items')
        read_only_fields = ('_id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }
    
    def get__id(self, obj):
        return base_utils.get_object_id_value(obj)

    def create(self, validated_data):
        user = self.context['request'].user
        instance, _ = cart_models.Cart.objects.get_or_create(user=user)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        items = validated_data.pop('items', None)
        if items is not None:
            items_in_db = instance.items.all()
            items_in_db.delete()
            for item_details in items:
                product = product_models.Item.objects.filter(_id=item_details['item']['_id'])
                if product.exists():
                    created_item = cart_models.CartItem.objects.create(
                        item=product.first(), quantity=item_details['quantity']
                    )
                    instance.items.add(created_item)
        return instance
