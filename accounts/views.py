from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import AppUserCreationForm
# Create your views here.

class AppUserCreateView(CreateView):
    form_class = AppUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')


