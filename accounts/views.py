from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.models import Group
from accounts.forms import AppUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

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


class MyProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/my-profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        rider = None
        rider_organized_rides = None
        rider_joined_rides = None
        rider_ride_reviews = None
        rider_help_requests = None

        if hasattr(user, 'rider'):
            rider = user.rider
            rider_organized_rides = rider.rides.all()
            rider_joined_rides = rider.ride_participants.all()
            rider_ride_reviews = rider.written_reviews.all()
            rider_help_requests = rider.help_requests.all()

        user_garages = user.garages.all()
        user_garage_reviews = user.garage_reviews.all()

        context['profile_user'] = user
        context['rider'] = rider
        context['rider_organized_rides'] = rider_organized_rides
        context['rider_joined_rides'] = rider_joined_rides
        context['rider_ride_reviews'] = rider_ride_reviews
        context['rider_help_requests'] = rider_help_requests
        context['user_garages'] = user_garages
        context['user_garage_reviews'] = user_garage_reviews

        return context
