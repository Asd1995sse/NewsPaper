import django_filters
from django import forms
from .models import Post, Author


class PostFilter(django_filters.FilterSet):
    # Поиск по названию (содержит)
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название'
    )

    # Поиск по имени автора
    author__user__username = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Имя автора'
    )

    # Фильтр по дате
    created_at__gt = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='Позже даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'created_at__gt']