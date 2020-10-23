from django.contrib import admin

# Register your models here.
from accounts.models import User, Employee

admin.site.register(User)
admin.site.register(Employee)
