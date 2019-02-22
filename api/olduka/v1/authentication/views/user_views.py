from rest_framework import generics, permissions

import olduka.v1.authentication.serializers.user_serializers as user_serializers


class CreateUserView(generics.CreateAPIView):
    """
    Create a User
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = user_serializers.UserSerializer
