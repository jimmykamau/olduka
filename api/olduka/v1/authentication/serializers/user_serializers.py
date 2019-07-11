from django.contrib.auth.models import User
from rest_framework import serializers

import olduka.v1.authentication.models as authentication_models
import olduka.v1.authentication.utils as authentication_utils


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = authentication_models.UserProfile
        exclude = ('user', 'jwt_secret')


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email',
            'password', 'user_profile'
        )
        required_fields = (
            'first_name', 'last_name',
            'email', 'password'
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'write_only': True}
        }

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "A user with the email address {} is already registered".format(
                    email)
            )
        return email

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_profile = validated_data.pop('user_profile', None)
        if validated_data.get('username') is None:
            validated_data['username'] = validated_data['email']
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.is_active = False
        user.save()
        authentication_models.UserProfile.objects.create(
            user=user, **user_profile
        )
        authentication_utils.send_account_confirmation_email(user)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user_profile = validated_data.pop('user_profile', None)
        instance.__dict__.update(validated_data)
        if password:
            instance.set_password(password)
            authentication_utils.send_password_changed_email(instance)
        if user_profile:
            instance.user_profile.__dict__.update(user_profile)
            instance.user_profile.save()
        instance.save()
        authentication_utils.send_account_details_changed_email(instance)
        return instance


class EmailValidationSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):
        email = value.lower()
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "The email address provided isn't registered to any account"
            )
        return email
