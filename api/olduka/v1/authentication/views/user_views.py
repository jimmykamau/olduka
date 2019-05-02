from django.contrib.auth.models import User
from rest_framework import generics, permissions, response, status

import olduka.v1.authentication.models as authentication_models
import olduka.v1.authentication.serializers.user_serializers as user_serializers
import olduka.v1.authentication.utils as authentication_utils


class CreateUserView(generics.CreateAPIView):
    """
    Create a User
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = user_serializers.UserSerializer


class RetrieveUpdateDestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update and Destroy a User
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = user_serializers.UserSerializer
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class LogoutUserView(generics.GenericAPIView):
    """
    Log out a user
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        authentication_utils.change_jwt_secret(request.user)
        return response.Response(
            {"detail": "User successfully logged out"},
            status=status.HTTP_200_OK
        )
