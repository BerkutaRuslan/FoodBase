from django.contrib import admin

# Register your models here.
from accounts.models import User, ResetKey, Employee

admin.site.register(User)
admin.site.register(Employee)
