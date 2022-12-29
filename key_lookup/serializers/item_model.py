from rest_framework import serializers
from key_lookup.models import ItemModel


class ItemModelAllSerializer(serializers.ModelSerializer):
    """
    Serializer for ItemModel CRUD operations

    Future Development: As project grows, I have seen use case of storing serializers inside of the
    specific views they are used in opposed to being modularized. Food for thought.
    """

    class Meta:
        model = ItemModel
        fields = '__all__'

