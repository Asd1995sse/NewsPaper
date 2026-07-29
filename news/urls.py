from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='list'),           # /news/
    path('<int:pk>/', views.news_detail, name='detail'),  # /news/1/
]