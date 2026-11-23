from django.urls import path
from services.views import (GarageCreateView,
                            GarageListView,
                            GarageDetailView,
                            GarageEditView,
                            GarageDeleteView,
                            GarageReviewCreateView,
                            GarageReviewListView,
                            GarageReviewDetailView, GarageReviewEditView, GarageReviewDeleteView,
                            )

app_name = 'services'

urlpatterns = [
    path('garage/create/', GarageCreateView.as_view(), name='garage_create'),

    path('garage/list/', GarageListView.as_view(), name='garage_list'),

    path('garage/details/<int:pk>/', GarageDetailView.as_view(), name='garage_details'),

    path('garage/edit/<int:pk>/', GarageEditView.as_view(), name='garage_edit'),

    path('garage/delete/<int:pk>/', GarageDeleteView.as_view(), name='garage_delete'),

    path('garage-review/create/', GarageReviewCreateView.as_view(), name='garage_review_create'),

    path('garage-review/list/', GarageReviewListView.as_view(), name='garage_review_list'),

    path('garage-review/details/<int:pk>/', GarageReviewDetailView.as_view(), name='garage_review_details'),


    path('garage-review/edit/<int:pk>/', GarageReviewEditView.as_view(), name='garage_review_edit'),

    path('garage-review/delete/<int:pk>/',GarageReviewDeleteView.as_view(), name='garage_review_delete'),



]