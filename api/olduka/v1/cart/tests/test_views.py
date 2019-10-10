from django.urls import reverse
from rest_framework.test import APITestCase

import olduka.v1.authentication.tests.factories as auth_factories
import olduka.v1.cart.models as cart_models
import olduka.v1.cart.tests.factories as cart_factories
import olduka.v1.utils as base_utils
from olduka.v1.cart import logger


class MongoDBTestClass(APITestCase):
    databases = '__all__'


class CreateCartViewTests(MongoDBTestClass):

    def setUp(self):
        self.user_profile = auth_factories.UserProfileFactory()
        self.client.force_authenticate(user=self.user_profile.user)
        self.cart = cart_factories.CartFactory(user=self.user_profile.user)
        self.cart_id = base_utils.get_object_id_value(self.cart)
        self.url = reverse('v1:create-cart')
    
    def tearDown(self):
        self.client.force_authenticate(user=None)
    
    def test_create_cart(self):
        # Check if multiple carts are created for the same user
        response = self.client.post(
            self.url, format='json'
        )
        self.assertEqual(
            self.cart_id, response.data['_id']
        )


class ModifyCartViewTests(MongoDBTestClass):

    def setUp(self):
        self.user_profile = auth_factories.UserProfileFactory()
        self.client.force_authenticate(user=self.user_profile.user)
        self.cart = cart_factories.CartFactory(user=self.user_profile.user)
        self.cart_id = base_utils.get_object_id_value(self.cart)
        self.url = reverse(
            'v1:modify-cart',
            kwargs={
                'pk': self.cart_id
            }
        )
    
    def test_retrieve_cart(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertCountEqual(
            ['_id', 'user', 'items'], response.data
        )
    
    def test_delete_cart(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(204, response.status_code)
        self.assertFalse(
            cart_models.Cart.objects.filter(_id=self.cart_id).exists()
        )
        self.assertFalse(
            cart_models.CartItem.objects.filter(
                cart___id=self.cart_id
            ).exists()
        )
