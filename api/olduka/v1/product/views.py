from rest_framework import generics, permissions

import olduka.v1.product.serializers as product_serializers
import olduka.v1.product.models as product_models


class ListCategoriesView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = product_serializers.CategorySerializer
    queryset = product_models.Category.objects.filter(parent__isnull=True)


class GetCategoryView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = product_serializers.CategorySerializer
    queryset = product_models.Category.objects.all()


class GetCategoryItemsView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = product_serializers.CategoryItemSerializer

    def get_queryset(self):
        category = self.kwargs['pk']
        return product_models.Category.objects.filter(pk=category)


class ListItemsView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = product_serializers.ItemSerializer
    queryset = product_models.Item.objects.all()


class GetItemView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = product_serializers.ItemSerializer
    queryset = product_models.Item.objects.all()
