from django.urls import path
from .views import ItemModelCreateOrList, ItemModelIncrement

urlpatterns = [
    path('', ItemModelCreateOrList.as_view(), name='create-item-or-list'),
    path('<int:item_key>/increment', ItemModelIncrement.as_view(), name='item-increment')
]
