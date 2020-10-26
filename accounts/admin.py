from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from accounts.models import User, Employee


class CustomEmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'salary', 'started_from', 'restaurant')
    fieldsets = (
        ('Personal info', {'fields': ('user', 'restaurant', 'department', 'salary')}),
    )


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone', )
    search_fields = ('first_name', 'last_name', 'email', 'phone')

    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'photo')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(User, CustomUserAdmin)
admin.site.register(Employee, CustomEmployeeAdmin)
