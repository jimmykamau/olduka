from django.contrib import admin

import olduka.v1.cart.models as cart_models

admin.site.register(cart_models.Cart)
admin.site.register(cart_models.CartItem)
