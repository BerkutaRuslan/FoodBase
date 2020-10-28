from django.conf import settings
from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from restaurant.models import Restaurant, RestaurantContacts


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'phone', 'work_from', 'work_to', 'latitude', 'longitude',)
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'work_from', 'work_to', 'description', 'days_to_review_employee_salary',
                       'latitude', 'longitude')
        }),
    )

    class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'js/admin/location_picker.js',
            )


@admin.register(RestaurantContacts)
class MyModelAdmin(admin.ModelAdmin, DynamicArrayMixin):
    fieldsets = (
        (None, {
            'fields': ('email', 'phone',)
        }),
    )
    pass
