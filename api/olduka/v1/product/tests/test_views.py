import factory
from django.urls import reverse
from rest_framework.test import APITestCase

import olduka.v1.product.tests.factories as product_factories
from olduka.v1.product import logger
import olduka.v1.product.utils as product_utils


class MongoDBTestClass(APITestCase):
    databases = '__all__'


class ListCategoriesViewTests(MongoDBTestClass):

    def setUp(self):
        self.categories = product_factories.CategoryFactory.create_batch(3)
        self.url = reverse('v1:list-categories')

    def test_list_categories(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            len(self.categories),
            len(response.data)
        )


class GetCategoryViewTests(MongoDBTestClass):

    def setUp(self):
        self.category = product_factories.SubcategoryFactory()
        self.url = reverse(
            'v1:get-category',
            kwargs={
                'pk': product_utils.get_object_id_value(self.category)
            }
        )
    
    def test_get_category(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertCountEqual(
            ['_id', 'name', 'description', 'image_url', 'subcategory'],
            response.data
        )
        self.assertEqual(
            self.category.description,
            response.data['description']
        )
