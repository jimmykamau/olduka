import factory
from django.contrib.auth.models import User
from factory import fuzzy

import olduka.v1.authentication.models as authentication_models


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall(
        'set_password', 'password'
    )


class UserProfileFactory(factory.DjangoModelFactory):

    class Meta:
        model = authentication_models.UserProfile

    user = factory.SubFactory(UserFactory)
    mobile = factory.Faker('msisdn')
