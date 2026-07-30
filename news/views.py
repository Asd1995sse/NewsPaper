from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import formset_factory
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm

# Create your views here.


# СТРАНИЦА СО СПИСКОМ НОВОСТЕЙ
def news_list(request):
    posts = Post.objects.filter(
        post_type=Post.NEWS
    ).order_by('-created_at')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'news_list.html', context)


# СТРАНИЦА ПОИСКА
def news_search(request):
    posts = Post.objects.filter(post_type=Post.NEWS).order_by('-created_at')
    filter = PostFilter(request.GET, queryset=posts)

    context = {
        'filter': filter,
    }
    return render(request, 'news_search.html', context)


# ДЕТАЛЬНАЯ СТРАНИЦА НОВОСТИ
def news_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, post_type=Post.NEWS)
    context = {'post': post}
    return render(request, 'news_detail.html', context)


# СОЗДАНИЕ НОВОСТИ
class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'
    success_url = reverse_lazy('news:list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        form.instance.post_type = Post.NEWS
        author, _ = Author.objects.get_or_create(user=self.request.user)
        form.instance.author = author
        return super().form_valid(form)


# РЕДАКТИРОВАНИЕ НОВОСТИ
class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news:list')
    permission_required = 'news.change_post'

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS)


# УДАЛЕНИЕ НОВОСТИ
class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news:list')
    permission_required = 'news.delete_post'

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS)


# СОЗДАНИЕ СТАТЬИ
class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('news:list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        form.instance.post_type = Post.ARTICLE  # Тип "статья"
        author, created = Author.objects.get_or_create(user=self.request.user)
        form.instance.author = author
        return super().form_valid(form)


# РЕДАКТИРОВАНИЕ СТАТЬИ
class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('news:list')
    permission_required = 'news.change_post'

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.ARTICLE)


# УДАЛЕНИЕ СТАТЬИ
class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('news:list')
    permission_required = 'news.delete_post'

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.ARTICLE)