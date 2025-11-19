from django.urls import path
from .views import CreateProductView, ListProductView, GetProductView, UpdateProductView, DeleteProductView

urlpatterns = [
    path('<int:pk>/', GetProductView.as_view(), name='get_product'),
    path('list/', ListProductView.as_view(), name='list_product'),
    path('add/', CreateProductView.as_view(), name='create_product'),
    path('<int:pk>/delete/', DeleteProductView.as_view(), name='delete_product'),
    path('<int:pk>/update/', UpdateProductView.as_view(), name='update_product')
]