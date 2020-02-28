import factory

import olduka.v1.authentication.tests.factories as auth_factories
import olduka.v1.payment.models as payment_models
import olduka.v1.payment.utils as payment_utils
import olduka.v1.product.tests.factories as product_factories


class InvoiceItemFactory(factory.DjangoModelFactory):

    class Meta:
        model = payment_models.InvoiceItem
    
    item = factory.SubFactory(product_factories.ItemFactory)
    quantity = factory.Faker('random_int', min=1, max=10)


class InvoiceFactory(factory.DjangoModelFactory):

    class Meta:
        model = payment_models.Invoice
    
    user = factory.SubFactory(auth_factories.UserFactory)
    status = 'OP'
    items = factory.RelatedFactoryList(InvoiceItemFactory, size=5)
    
    @factory.post_generation
    def invoice_total(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            return payment_utils.get_item_totals(extracted.items)
