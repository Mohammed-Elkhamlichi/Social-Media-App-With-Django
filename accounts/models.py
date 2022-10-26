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
    following = models.ManyToManyField(

        'User',
        related_name="user_following",
        null=True, blank=True
    )
    followers = models.ManyToManyField(
        'User',
        related_name="user_followers",
        null=True,
        blank=True
    )
    profile_pic = models.ImageField(
        upload_to='profile/%Y/%m/%d/',
        blank=True,
        null=True,
        default="profile/avatar.png"
    )
    bio = models.TextField(null=True, blank=True)
    phone = models.IntegerField(unique=True, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username.capitalize()
