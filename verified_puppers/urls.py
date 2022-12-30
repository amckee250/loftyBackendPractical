from django.urls import path
from .views import DogDetail

urlpatterns = [
    path('<int:pk>', DogDetail.as_view(), name='dog-detail')
]
