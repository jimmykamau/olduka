from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

import olduka.v1.authentication.models as authentication_models
import olduka.v1.authentication.tests.factories as authentication_factories


class CreateUserViewTests(APITestCase):

    def setUp(self):
        self.user_profile = authentication_factories.UserProfileFactory.build()
        self.user = self.user_profile.user
        self.user_profile_data = dict(
            username=self.user.username,
            first_name=self.user.first_name,
            last_name=self.user.last_name,
            email=self.user.email,
            password=self.user.password,
            user_profile={
                "mobile": self.user_profile.mobile
            }
        )
        self.url = reverse('v1:create-user')

    def tearDown(self):
        self.client.force_authenticate(user=None)

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


class AuthorizationTests(APITestCase):

    def setUp(self):
        self.user_profile = authentication_factories.UserProfileFactory.create()
        self.user_details = dict(
            username=self.user_profile.user.username,
            password="12345"
        )
        self.user_profile.user.set_password(self.user_details['password'])
        self.user_profile.user.save()
        self.url = reverse('v1:login')
        self.login_response = self.client.post(
            self.url, self.user_details, format='json')
        self.auth_token = self.login_response.data['token']
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {}'.format(self.auth_token))

    def test_logging_in(self):
        self.assertEqual(200, self.login_response.status_code)
        self.assertCountEqual(['token', 'user'], self.login_response.data)
        response = self.client.get(
            reverse('v1:user', kwargs={'pk': self.user_profile.user.id}),
            format='json'
        )
        self.assertEqual(200, response.status_code)

    def test_logging_out(self):
        response = self.client.get(reverse('v1:logout'), format='json')
        self.assertEqual(200, response.status_code)
        response = self.client.get(
            reverse('v1:user', kwargs={'pk': self.user_profile.user.id}),
            format='json'
        )
        self.assertEqual(401, response.status_code)


class RetrieveUpdateDestroyUserViewTests(APITestCase):

    def setUp(self):
        self.user_profile = authentication_factories.UserProfileFactory.create()
        self.client.force_authenticate(user=self.user_profile.user)
        self.url = reverse('v1:user', kwargs={'pk': self.user_profile.user.id})

    def tearDown(self):
        self.client.force_authenticate(user=None)

    def test_get_user(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.user_profile.user.email, response.data['email'])

    def test_update_user(self):
        new_user_data = dict(
            first_name="John",
            last_name="Doe"
        )
        response = self.client.patch(self.url, new_user_data, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue(
            User.objects.filter(
                first_name=new_user_data['first_name'],
                last_name=new_user_data['last_name']
            )
        )

    def test_change_password(self):
        """
        This is mostly used to check if Celery is sending password-change emails correctly.
        Confirm this through the Celery logs.
        """
        new_user_data = dict(password="abcde")
        response = self.client.patch(self.url, new_user_data, format='json')
        self.assertEqual(200, response.status_code)

    def test_delete_user(self):
        self.client.force_authenticate(user=None)
        user_details = dict(
            username=self.user_profile.user.username,
            password="12345"
        )
        self.user_profile.user.set_password(user_details['password'])
        self.user_profile.user.save()
        auth_token_response = self.client.post(
            reverse('v1:login'), user_details, format='json'
        )
        jwt_token = auth_token_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(jwt_token))
        response = self.client.delete(self.url, format='json')
        self.assertEqual(204, response.status_code)
        # Confirm that the user hasn't actually been deleted
        self.assertTrue(
            User.objects.filter(
                email=self.user_profile.user.email
            ).exists()
        )
        # Check that the user is inactive
        self.assertFalse(
            User.objects.get(
                email=self.user_profile.user.email
            ).is_active
        )
        user_details_response = self.client.get(self.url, format='json')
        self.assertEqual(401, user_details_response.status_code)
        # Confirm the user can't log in
        auth_token_response = self.client.post(
            reverse('v1:login'), user_details, format='json'
        )
        self.assertEqual(400, auth_token_response.status_code)


class ValidateEmailViewTests(APITestCase):

    def setUp(self):
        self.user_profile = authentication_factories.UserProfileFactory.create()
        self.url = reverse('v1:validate-email')

    def test_validate_email(self):
        """
        Checks if the task is executed without errors
        """
        email_address = dict(email=self.user_profile.user.email)
        response = self.client.post(self.url, email_address, format='json')
        self.assertEqual(200, response.status_code)

    def test_validate_unregistered_email(self):
        email_address = dict(email="jdoe@example.com")
        response = self.client.post(self.url, email_address, format='json')
        self.assertEqual(400, response.status_code)
