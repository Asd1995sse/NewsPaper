from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.



def news_list(request):
    """Список всех новостей (только тип NEWS), отсортированных по дате"""
    posts = Post.objects.filter(
        post_type=Post.NEWS
    ).order_by('-created_at')  # от свежих к старым

    context = {
        'posts': posts,
    }
    return render(request, 'news_list.html', context)


def news_detail(request, pk):
    """Детальная страница новости"""
    post = get_object_or_404(Post, pk=pk, post_type=Post.NEWS)

    context = {
        'post': post,
    }
    return render(request, 'news_detail.html', context)