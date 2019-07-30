from djongo import models


class Category(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='subcategory'
    )

    def __str__(self):
        return self.name


class Price(models.Model):
    price = models.FloatField()
    discount = models.FloatField()

    class Meta:
        abstract = True


class ProductImage(models.Model):
    image_url = models.URLField()

    class Meta:
        abstract = True


class Item(models.Model):
    _id = models.ObjectIdField()
    category = models.ArrayReferenceField(
        to=Category,
        on_delete=models.CASCADE,
        related_name='category_item'
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    images = models.ArrayModelField(
        model_container=ProductImage
    )
    price = models.EmbeddedModelField(
        model_container=Price
    )

    objects = models.DjongoManager()

    def __str__(self):
        return self.name
