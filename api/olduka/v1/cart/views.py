from rest_framework import generics, permissions

import olduka.v1.cart.models as cart_models
import olduka.v1.cart.serializers as cart_serializers


class CreateCartView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = cart_serializers.CartSerializer


class RetrieveUpdateDestroyCartView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = cart_serializers.CartSerializer
    queryset = cart_models.Cart.objects.all()

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)
