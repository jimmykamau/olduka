from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

app_name = 'v1'
schema_view = get_swagger_view(title='Olduka')

urlpatterns = [
    path('', schema_view),
    path('auth/', include('olduka.v1.authentication.urls')),
    path('product/', include('olduka.v1.product.urls')),
    path('cart/', include('olduka.v1.cart.urls')),
    path('payment/', include('olduka.v1.payment.urls'))
]
