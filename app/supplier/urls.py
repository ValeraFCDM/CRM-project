from django.urls import path
from .views import CreateSupplierView, ListSupplierView, UpdateSupplierView, DeleteSupplierView

urlpatterns = [
    path('list/', ListSupplierView.as_view(), name='list_supplier'),
    path('create/', CreateSupplierView.as_view(), name='create_supplier'),
    path('<int:pk>/delete/', DeleteSupplierView.as_view(), name='delete_supplier'),
    path('<int:pk>/update/', UpdateSupplierView.as_view(), name='update_supplier'),
]