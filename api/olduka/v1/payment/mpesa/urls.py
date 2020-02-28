from django.urls import path

import olduka.v1.payment.mpesa.views as mpesa_views


urlpatterns = [
    path(
        '',
        mpesa_views.InitiatePaymentView.as_view(),
        name='initiate-payment'
    ),
    path(
        'callback/',
        mpesa_views.MpesaCallbackView.as_view(),
        name='mpesa-callback')
]
