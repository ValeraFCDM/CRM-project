from django.urls import path
from .views import GetStorageView, CreateStorageView, DeleteStorageView, UpdateStorageView

urlpatterns = [
    path('<int:pk>/', GetStorageView.as_view(), name='get_storage'),
    path('create/', CreateStorageView.as_view(), name='create_storage'),
    path('<int:pk>/delete/', DeleteStorageView.as_view(), name='delete_storage'),
    path('<int:pk>/update/', UpdateStorageView.as_view(), name='update_storage'),
]