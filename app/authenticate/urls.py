from django.urls import path
from .views import UserRegisterView, UserAttachView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name='register'),
    path("attach-user-to-company/", UserAttachView.as_view(), name='attach_to_company'),
]
