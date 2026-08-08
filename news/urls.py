from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Новости
    path('', views.news_list, name='list'),
    # Расширенная страница новостей
    path('<int:pk>/', views.news_detail, name='detail'),
    # Поиск
    path('search/', views.news_search, name='search'),
    # CRUD для новостей
    path('create/', views.NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    # CRUD для статей
    path('articles/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('category/<int:category_id>/subscribe/', views.subscribe_to_category, name='subscribe_category'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
]