from rest_framework import serializers

import olduka.v1.payment.models as payment_models
import olduka.v1.payment.mpesa.models as mpesa_models
import olduka.v1.payment.mpesa.tasks as mpesa_tasks
import olduka.v1.payment.serializers as payment_serializers
import olduka.v1.payment.utils as payment_utils


class InitiatePaymentSerializer(serializers.ModelSerializer):

    invoice = payment_serializers.InvoiceSerializer(required=False)
    invoice_id = serializers.CharField(required=False)

    class Meta:
        model = mpesa_models.MpesaPayment
        fields = (
            'invoice', 'invoice_id', 'phone_number'
        )
    
    def create(self, validated_data):
        invoice = payment_models.Invoice.objects.get(_id=validated_data['invoice_id'])
        instance, _ = mpesa_models.MpesaPayment.objects.get_or_create(
            invoice=invoice
        )
        instance.amount = payment_utils.get_item_totals(invoice.items)
        instance.phone_number = validated_data['phone_number']
        instance.save()
        mpesa_tasks.initiate_mpesa_payment.delay(instance.pk)
        return instance


class MetadataItemSerializer(serializers.Serializer):
    Name = serializers.CharField()
    Value = serializers.CharField(required=False)


class CallbackMetadataSerializer(serializers.Serializer):
    Item = MetadataItemSerializer(many=True)


class StkCallbackSerializer(serializers.Serializer):
    MerchantRequestID = serializers.CharField()
    CheckoutRequestID = serializers.CharField()
    ResultDesc = serializers.CharField()
    CallbackMetadata = CallbackMetadataSerializer(required=False)


class CallbackResultSerializer(serializers.Serializer):
    stkCallback = StkCallbackSerializer(required=False)


class CallbackSerializer(serializers.Serializer):
    Body = CallbackResultSerializer()
