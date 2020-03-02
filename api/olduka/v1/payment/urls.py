from django.urls import include, path

import olduka.v1.payment.views as payment_views


urlpatterns = [
    path('', payment_views.ListCreateInvoiceView.as_view(), name='invoice'),
    path('mpesa/', include('olduka.v1.payment.mpesa.urls'))
]
