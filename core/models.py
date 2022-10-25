from django.db import models
from accounts.models import User
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def is_user_joined(self, request):
        for user in self.users.all():
            if user == request.user:
                return True
        return False


class Room(models.Model):
    host = models.ForeignKey(
        User,  on_delete=models.CASCADE, blank=True)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[:50]
