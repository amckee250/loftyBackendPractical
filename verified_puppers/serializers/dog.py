from rest_framework import serializers
from verified_puppers.models import Dog


class DogAllSerializer(serializers.ModelSerializer):
    """
    Serializer for basic Dog CRUD operations

    Future Development: As project grows, I have seen use case of storing serializers inside of the
    specific views they are used in opposed to being modularized. Food for thought.
    """

    class Meta:
        model = Dog
        fields = '__all__'


class DogCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for Dog create usage
    """

    class Meta:
        model = Dog
        fields = ['original_img']

    def create(self, validated_data):
        return Dog(**validated_data)
