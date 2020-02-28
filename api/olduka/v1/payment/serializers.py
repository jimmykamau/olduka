from django.contrib.sites.models import Site
from rest_framework import serializers

import olduka.v1.authentication.serializers.user_serializers as user_serializers
import olduka.v1.payment.models as payment_models
import olduka.v1.payment.utils as payment_utils
import olduka.v1.product.models as product_models
import olduka.v1.product.serializers as product_serializers
import olduka.v1.utils as base_utils

CURRENT_SITE = Site.objects.get_current()


class InvoiceItemSerializer(serializers.ModelSerializer):
    item = product_serializers.ItemSerializer()

    class Meta:
        model = payment_models.InvoiceItem
        fields = ('item', 'quantity')


class InvoiceSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    user = user_serializers.UserSerializer(required=False)
    items = InvoiceItemSerializer(many=True, required=True)
    invoice_total = serializers.SerializerMethodField()

    class Meta:
        model = payment_models.Invoice
        fields = (
            '_id', 'user', 'items', 'invoice_total',
            'status', 'created_at'
        )
        read_only_fields = ('_id', 'user', 'status', 'invoice_total')
        extra_kwargs = {
            'user': {'write_only': True}
        }
    
    def get__id(self, obj):
        return base_utils.get_object_id_value(obj)
    
    def get_invoice_total(self, obj):
        return payment_utils.get_item_totals(obj.items)
    
    def create(self, validated_data):
        user = self.context['request'].user
        instance, created = payment_models.Invoice.objects.get_or_create(
            user=user, status='OP'
        )
        if not created:
            instance.items.clear()
        for item in validated_data['items']:
            product = product_models.Item.objects.filter(_id=item['item']['_id'])
            if product.exists():
                invoice_item = payment_models.InvoiceItem.objects.create(
                    item=product.first(), quantity=item['quantity']
                )
                instance.items.add(invoice_item)
        instance.quantities_updated = False
        instance.save()
        email_subject = f"Your {CURRENT_SITE.name} invoice has been created"
        email_body = f"Invoice {base_utils.get_object_id_value(instance)} has been created."
        payment_utils.send_invoice_email(instance, email_subject, email_body)
        return instance
