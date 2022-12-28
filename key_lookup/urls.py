from django.urls import path, include
from .views import ItemModelCreateOrList

urlpatterns = [
    path('', ItemModelCreateOrList.as_view(), name='item')

]

