from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    profile_pic = models.ImageField(
        upload_to=f"profile/", height_field=None, width_field=None, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    phone = models.IntegerField(unique=True, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username.capitalize()
