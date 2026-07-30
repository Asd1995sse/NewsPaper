from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import BaseRegisterForm
from django.contrib.auth.models import User

# Create your views here.

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = reverse_lazy('account_login')
    template_name = 'sign/register.html'