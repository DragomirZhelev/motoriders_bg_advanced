from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import Group
from accounts.forms import AppUserCreationForm
# Create your views here.

class AppUserCreateView(CreateView):
    form_class = AppUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        registered_users_group = Group.objects.get(name='Registered Users')


        self.object.groups.add(registered_users_group)

        return response

class AppUserLoginView(LoginView):
    template_name = 'accounts/login.html'


class AppUserLogoutView(LogoutView):
    next_page = '/'


