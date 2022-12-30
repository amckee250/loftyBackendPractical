from rest_framework.generics import RetrieveAPIView

from verified_puppers.serializers import DogAllSerializer
from verified_puppers.models import Dog


class DogDetail(RetrieveAPIView):
    """
    View to query Dog model detail data

    Note: View access is open, no need to be logged in
    """
    queryset = Dog.objects.all()
    serializer_class = DogAllSerializer
