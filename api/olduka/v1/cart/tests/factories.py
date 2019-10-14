import factory

import olduka.v1.authentication.tests.factories as auth_factories
import olduka.v1.cart.models as cart_models
import olduka.v1.product.tests.factories as product_factories


class CartItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = cart_models.CartItem
    
    item = factory.SubFactory(product_factories.ItemFactory)
    quantity = factory.Faker('random_int', min=1, max=10)


class CartFactory(factory.DjangoModelFactory):
    class Meta:
        model = cart_models.Cart
    
    user = factory.SubFactory(auth_factories.UserFactory)
    
    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for item in extracted:
                self.items.add(item)
