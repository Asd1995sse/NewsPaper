from django.urls import path
from .views import upgrade_me

app_name = 'protect'

urlpatterns = [
    path('upgrade/', upgrade_me, name='upgrade'),
]