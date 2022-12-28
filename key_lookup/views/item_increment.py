from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from key_lookup.serializers import ItemModelSerializer
from key_lookup.models import ItemModel


class ItemModelIncrement(APIView):
    """
    View to query and increment a ItemModels' value by given amount

    Note: Must be logged in (via admin panel session) to increment
    """
    # permission_classes = [IsAuthenticated]

    def patch(self, request, item_key):
        print(item_key)
        try:
            item_obj = get_object_or_404(ItemModel, item_key=str(item_key))
            print(item_obj)
            increment_amount = request.data.get('increment_amount')
            print(increment_amount)

            item_obj.increment_value(increment_amount)

            return Response(ItemModelSerializer(item_obj).data, status=status.HTTP_200_OK)

        except TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)