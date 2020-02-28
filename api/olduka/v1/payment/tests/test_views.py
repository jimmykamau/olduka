from django.urls import reverse
from rest_framework.test import APITestCase

import olduka.v1.authentication.tests.factories as auth_factories
import olduka.v1.payment.tests.factories as payment_factories
import olduka.v1.utils as base_utils
from olduka.v1.payment import logger


class MongoDBTestClass(APITestCase):
    databases = '__all__'


class InvoiceViewTests(MongoDBTestClass):

    def setUp(self):
        self.user_profile = auth_factories.UserProfileFactory()
        self.client.force_authenticate(user=self.user_profile.user)
        self.invoice = payment_factories.InvoiceFactory.build(
            user=self.user_profile.user)
        self.invoice_id = base_utils.get_object_id_value(self.invoice)
        self.url = reverse('v1:invoice')

    def tearDown(self):
        self.client.force_authenticate(user=None)

    def test_create_invoice(self):
        logger.debug(self.invoice.__dict__)
