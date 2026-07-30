from django.urls import path
from .views import BaseRegisterView

app_name = 'sign'

urlpatterns = [
    path('register/', BaseRegisterView.as_view(), name='register'),
]