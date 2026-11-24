from django.urls import path
from accounts.views import AppUserCreateView, AppUserLoginView, AppUserLogoutView, MyProfileView

app_name = 'accounts'

urlpatterns = [
    path('register/', AppUserCreateView.as_view(), name='register'),
    path('login/', AppUserLoginView.as_view(), name='login'),

    path('logout/', AppUserLogoutView.as_view(), name='logout'),

    path('my-profile/', MyProfileView.as_view(), name='my_profile'),



]


