from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField


class ContactQuery(models.Model):
    name = models.CharField(max_length=60, null=True)
    email = models.EmailField(max_length=50, null=True)
    subject = models.CharField(max_length=30, null=True)
    query = models.TextField()


class UserAddress(models.Model):
    label = models.CharField(max_length=20, default="Home")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    landmark = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = CountryField(blank_label='(select country)')
    pincode = models.IntegerField(max_length=6, null=True)
    mobile = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'label']

