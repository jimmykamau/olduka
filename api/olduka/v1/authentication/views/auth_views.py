from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404, redirect
from itsdangerous import (BadData, BadSignature, SignatureExpired,
                          URLSafeTimedSerializer)
from rest_framework import generics, permissions


class ValidateEmailView(generics.GenericAPIView):
    """
    Validate a user's email address
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        error_url = request.build_absolute_uri(settings.EMAIL_VERIFICATION_ERROR_URL)
        success_url = request.build_absolute_uri(settings.EMAIL_VERIFICATION_SUCCESS_URL)
        token_expired_url = error_url
        if settings.TOKEN_EXPIRED_URL:
            token_expired_url = request.build_absolute_uri(settings.TOKEN_EXPIRED_URL)
        token_serializer = URLSafeTimedSerializer(settings.SECRET_KEY, "auth")
        token = request.query_params.get('token', None)
        if token is None:
            return redirect(error_url)
        try:
            email_address = token_serializer.loads(
                token, max_age=600)  # Ten minutes
            user = User.objects.filter(email=email_address)
            if user is None:
                return redirect(error_url)
            user = user.first()
            user.is_active = True
            user.save()
            return redirect(success_url)
        except SignatureExpired:
            return redirect(token_expired_url)
        except (BadData, BadSignature):
            return redirect(error_url)
