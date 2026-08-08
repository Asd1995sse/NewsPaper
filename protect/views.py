from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from news.models import Author


# Create your views here.

@login_required
def upgrade_me(request):
    user = request.user
    authors_group, created = Group.objects.get_or_create(name='authors')

    if user.groups.filter(name='authors').exists():
        messages.info(request, 'Вы уже являетесь автором.')

    else:
        authors_group.user_set.add(user)
        author, _ = Author.objects.get_or_create(user=user)
        messages.success(request, 'Теперь вы автор!')

    return redirect('/news/')