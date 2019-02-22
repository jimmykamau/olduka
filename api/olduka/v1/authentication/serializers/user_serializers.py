from django.contrib.auth.models import User
from rest_framework import serializers

import olduka.v1.authentication.models as authentication_models


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = authentication_models.UserProfile
        exclude = ('user',)


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
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
        password = validated_data.pop('password')
        user_profile = validated_data.pop('user_profile')
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
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.__dict__.update(validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        user_profile = validated_data.get('user_profile')
        if user_profile:
            instance.user_profile.__dict__.update(user_profile)
        return instance
