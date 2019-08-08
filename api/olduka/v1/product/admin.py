from django.contrib import admin

import olduka.v1.product.models as product_models

admin.site.register(product_models.Category)
admin.site.register(product_models.Item)
