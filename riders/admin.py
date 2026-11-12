from django.contrib import admin
from riders.models import Rider


# Register your models here.

@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = [
        # 'first_name',
        # 'last_name',
        'user',
        'nickname',
        'city',
        'motorcycle_brand',
        'motorcycle_type'
    ]

    list_filter = [
        # 'first_name',
        # 'last_name',
        'nickname',
        'city',
        'motorcycle_brand',
        'motorcycle_type'
    ]

    search_fields = [
        'user__first_name',
        'user__last_name',
        'nickname',
        'city',
        'motorcycle_brand',
        'motorcycle_type'
    ]



# Register your models here.
