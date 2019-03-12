import olduka.v1.authentication.models as authentication_models
import olduka.v1.authentication.serializers.user_serializers as user_serializers
from django.contrib.auth.models import User
from rest_framework import generics, permissions


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
