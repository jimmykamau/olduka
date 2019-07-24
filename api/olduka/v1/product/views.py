from rest_framework import generics, permissions

import olduka.v1.product.serializers as product_serializers
import olduka.v1.product.models as product_models


class ListItemsView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = product_serializers.ItemSerializer
    queryset = product_models.Item.objects.all()
