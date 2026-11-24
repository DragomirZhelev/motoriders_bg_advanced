from django.contrib import admin
from services.models import Service, Garage, GarageReview
# Register your models here.

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(Garage)
class GarageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(GarageReview)
class GarageReviewAdmin(admin.ModelAdmin):
    list_display = ('garage', 'reviewer', 'rating')
    list_filter = ('garage', 'reviewer', 'rating')
    search_fields = ('garage__name', 'reviewer__nickname', 'reviewer__user__first_name', 'reviewer__user__last_name')
