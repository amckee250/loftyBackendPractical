from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from key_lookup.serializers import ItemModelSerializer
from key_lookup.models import ItemModel


class ItemModelCreateOrList(generics.ListCreateAPIView):
    """
    ViewSet to Create and List API endpoint for ItemModel

    Note: Open to read only, must be logged in (via session) to create
    """
    queryset = ItemModel.objects.all()
    serializer_class = ItemModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
