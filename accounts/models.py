from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField

from FoodBase import settings
from FoodBase.utils import generate_token
from restaurant.models import Restaurant

department_choices = (
    ('security', 'security'),
    ('cleaner', 'cleaner'),
    ('cook', 'cook'),
    ('manager', 'manager'),
    ('main_head', 'main_head'),
)


class User(AbstractUser):
    first_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(max_length=254, null=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True, help_text="phone as username")
    passcode = models.CharField(max_length=4, null=True, blank=True)
    passcode_timer = models.DateTimeField(null=True)
    photo = models.ImageField(upload_to='users', default=settings.USER_DEFAULT_IMAGE)
    address = models.CharField(max_length=250, blank=True)
    balance = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class ResetKey(models.Model):
    user = models.ForeignKey(User, related_name='reset_key', on_delete=models.CASCADE)
    reset_key = models.CharField(max_length=40, default=generate_token)

    class Meta:
        verbose_name_plural = 'Reset key'


class Employee(models.Model):
    user = models.ForeignKey(User, related_name='employees', on_delete=models.CASCADE)
    salary = models.FloatField()
    department = models.CharField(max_length=100, choices=department_choices)
    started_from = models.DateField(auto_now_add=True)
    restaurant = models.ForeignKey(Restaurant, related_name='employees', on_delete=models.CASCADE)
    review_date = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Employee'
