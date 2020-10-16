from django_better_admin_arrayfield.models.fields import ArrayField
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    email = ArrayField(models.EmailField(max_length=254), blank=True, null=True,)
    description = models.TextField(max_length=2000)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    work_from = models.TimeField()
    work_to = models.TimeField()
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name


class RestaurantContacts(Restaurant):

    class Meta:
        proxy = True
        verbose_name_plural = 'Restaurant Contacts'
