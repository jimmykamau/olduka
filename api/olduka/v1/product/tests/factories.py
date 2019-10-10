import factory

import olduka.v1.product.models as product_models


class CategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = product_models.Category

    name = factory.Faker('word')
    description = factory.Faker('paragraph')
    image_url = factory.Faker('image_url')


class SubcategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = product_models.Category

    name = factory.Faker('word')
    description = factory.Faker('paragraph')
    image_url = factory.Faker('image_url')
    parent = factory.SubFactory(CategoryFactory)


class PriceFactory(factory.DjangoModelFactory):

    class Meta:
        model = product_models.Price

    price = factory.Faker('random_int', min=100)
    discount = factory.Faker('random_int', min=0, max=99)


class ProductImageFactory(factory.DjangoModelFactory):

    class Meta:
        model = product_models.ProductImage

    image_url = factory.Faker('image_url')

#  TODO: Check why this keeps returning None
class ItemFactory(factory.DjangoModelFactory):

    class Meta:
        model = product_models.Item

    category = factory.SubFactory(SubcategoryFactory)
    name = factory.Faker('word')
    description = factory.Faker('paragraph')
    images = factory.SubFactory(ProductImageFactory)
    price = factory.SubFactory(PriceFactory)
