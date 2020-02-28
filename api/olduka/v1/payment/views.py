from rest_framework import generics, permissions

import olduka.v1.payment.models as payment_models
import olduka.v1.payment.serializers as payment_serializers


class ListCreateInvoiceView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = payment_serializers.InvoiceSerializer
    queryset = payment_models.Invoice.objects.all()

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)
