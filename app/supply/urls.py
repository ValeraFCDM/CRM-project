from django.urls import path
from .views import CreateSupplyView, ListSupplyView

urlpatterns = [
    path('list/', ListSupplyView.as_view(), name='list_supply'),
    path('create/', CreateSupplyView.as_view(), name='create_supply'),
]