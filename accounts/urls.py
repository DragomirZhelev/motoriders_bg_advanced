from django.urls import path
from accounts.views import AppUserCreateView, AppUserLoginView, AppUserLogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', AppUserCreateView.as_view(), name='register'),
    path('login/', AppUserLoginView.as_view(), name='login'),

    path('logout/', AppUserLogoutView.as_view(), name='logout'),


]


