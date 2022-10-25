from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.


class Follower(models.Model):
    


class User(AbstractUser):
    get_date = datetime.datetime.now()
    year = get_date.year
    month = get_date.month
    day = get_date.day
    hour = get_date.hour
    second = get_date.second
    minute = get_date.minute
    followers = models.ManyToManyField(Follower, null=True, blank=True)

    profile_pic=models.ImageField(
        upload_to=f"profile/{day}-{month}-{year}/{hour}-{minute}-{second}", blank=True, null=True, default="profile/avatar.png")
    bio=models.TextField(null=True, blank=True)
    phone=models.IntegerField(unique=True, blank=True, null=True)
    country=models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username.capitalize()
