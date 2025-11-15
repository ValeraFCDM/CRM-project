from django.urls import path
from .views import GetCompanyView, CreateCompanyView, DeleteCompanyView, UpdateCompanyView

urlpatterns = [
    path('<int:pk>/', GetCompanyView.as_view(), name='get_company'),
    path('create/', CreateCompanyView.as_view(), name='create_company'),
    path('delete/', DeleteCompanyView.as_view(), name='delete_company'),
    path('update/', UpdateCompanyView.as_view(), name='update_company'),
]
