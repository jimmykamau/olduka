from django.contrib.auth.models import User
from djongo import models

import olduka.v1.product.models as product_models


class CartItem(models.Model):
    item = models.ForeignKey(
        product_models.Item,
        on_delete=models.CASCADE,
        related_name='cart_item'
    )
    quantity = models.IntegerField()


class Cart(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_cart'
    )
    items = models.ArrayReferenceField(
        to=CartItem,
        on_delete=models.SET_NULL,
        related_name='cart',
        null=True
    )
