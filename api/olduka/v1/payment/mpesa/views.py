from rest_framework import generics, permissions, response, status

import olduka.v1.payment.mpesa.models as mpesa_models
import olduka.v1.payment.mpesa.serializers as mpesa_serializers
from olduka.v1.payment import logger
import olduka.v1.payment.mpesa.tasks as mpesa_tasks


class InitiatePaymentView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = mpesa_serializers.InitiatePaymentSerializer


class MpesaCallbackView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = mpesa_serializers.CallbackSerializer

    def post(self, request):
        serializer = mpesa_serializers.CallbackSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data['Body']['stkCallback']
            payment = mpesa_models.MpesaPayment.objects.get(
                merchant_request_id=data['MerchantRequestID'],
                checkout_request_id=data['CheckoutRequestID']
            )
            payment.response_description = data['ResultDesc']
            payment.save()
            metadata = data.get('CallbackMetadata', None)
            if metadata:
                payment_info = {
                    k: v for k, v in [
                        a for a in list(
                            d.values() for d in metadata['Item']
                        ) if len(a) > 1
                    ]
                }
                payment_info['payment_pk'] = payment.pk
                mpesa_tasks.process_mpesa_payment.delay(payment_info)
        else:
            logger.warning(serializer.errors)
        return response.Response(
            status=status.HTTP_201_CREATED
        )
