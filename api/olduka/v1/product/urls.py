from django.urls import include, path

import olduka.v1.product.views as product_views

urlpatterns = [
    path(
        'item/',
        product_views.ListItemsView.as_view(),
        name='list-items'
    )
]
