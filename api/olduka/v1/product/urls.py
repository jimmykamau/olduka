from django.urls import include, path

import olduka.v1.product.views as product_views

urlpatterns = [
    path(
        'category/',
        product_views.ListCategoriesView.as_view(),
        name='list-categories'
    ),
    path(
        'category/<slug:pk>/',
        product_views.GetCategoryView.as_view(),
        name='get-category'
    ),
    path(
        'category/<slug:pk>/item/',
        product_views.GetCategoryItemsView.as_view(),
        name='get-category-items'
    ),
    path(
        'item/',
        product_views.ListItemsView.as_view(),
        name='list-items'
    ),
    path(
        'item/<slug:pk>/',
        product_views.GetItemView.as_view(),
        name='get-item'
    )
]
