from django.urls import include, path

import olduka.v1.cart.views as cart_views

urlpatterns = [
    path(
        'create/',
        cart_views.CreateCartView.as_view(),
        name='create-cart'
    ),
    path(
        '<slug:pk>/',
        cart_views.RetrieveUpdateDestroyCartView.as_view(),
        name='modify-cart'
    )
]
