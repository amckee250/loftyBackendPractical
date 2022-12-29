from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from key_lookup.serializers import ItemModelAllSerializer
from key_lookup.models import ItemModel


class ItemModelIncrement(APIView):
    """
    View to query and increment a ItemModels' value by given amount

    Note: Must be logged in (via session) to increment
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_key):
        """
        Note: Chose PATCH request based on the following doc https://www.rfc-editor.org/rfc/rfc2068#section-19.6.1
        Very curious to see what you all would think is best practice.
        """
        try:
            # Query/Get Data
            item_obj = get_object_or_404(ItemModel, item_key=str(item_key))
            increment_amount = request.data.get('increment_amount')

            # Validate
            if increment_amount < 1:
                raise ValueError

            # Update and return
            item_obj.increment_value(increment_amount)
            return Response(ItemModelAllSerializer(item_obj).data, status=status.HTTP_200_OK)

        except (TypeError, ValueError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
