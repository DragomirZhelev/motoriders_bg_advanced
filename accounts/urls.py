from django.urls import path
from accounts.views import AppUserCreateView

app_name = 'accounts'

urlpatterns = [
    path('register/', AppUserCreateView.as_view(), name='register'),
]


