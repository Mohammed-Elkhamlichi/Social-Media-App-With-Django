from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.


class User(AbstractUser):
    get_date = datetime.datetime.now()
    year = get_date.year
    month = get_date.month
    day = get_date.day
    hour = get_date.hour
    second = get_date.second
    minute = get_date.minute

    profile_pic = models.ImageField(
        upload_to=f"profile/", blank=True, null=True, default="profile/avatar.png")
    bio = models.TextField(null=True, blank=True)
    phone = models.IntegerField(unique=True, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username.capitalize()
