from django.contrib import admin

import olduka.v1.payment.models as payment_models
import olduka.v1.payment.mpesa.models as mpesa_models

admin.site.register(payment_models.Invoice)
admin.site.register(payment_models.InvoiceItem)

# Payment processors
admin.site.register(mpesa_models.MpesaPayment)
