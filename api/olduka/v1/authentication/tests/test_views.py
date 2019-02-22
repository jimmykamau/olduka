from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
import factory

import olduka.v1.authentication.models as authentication_models
import olduka.v1.authentication.tests.factories as authentication_factories


class CreateUserViewTests(APITestCase):

    def setUp(self):
        self.user_profile = authentication_factories.UserProfileFactory.build()
        self.user = self.user_profile.user
        self.user_profile_data = dict(
            username = self.user.username,
            first_name = self.user.first_name,
            last_name = self.user.last_name,
            email = self.user.email,
            password = self.user.password,
            user_profile = {
                "mobile": self.user_profile.mobile
            }
        )
        self.url = reverse('v1:create-user')

    def test_create_user(self):
        response = self.client.post(
            self.url, self.user_profile_data, format='json'
        )
        self.assertEqual(201, response.status_code)
        self.assertTrue(
            User.objects.filter(
                email=self.user_profile_data.get('email')
            ).exists()
        )
        self.assertTrue(
            authentication_models.UserProfile.objects.filter(
                mobile=self.user_profile_data.get('user_profile').get('mobile') 
            )
        )
