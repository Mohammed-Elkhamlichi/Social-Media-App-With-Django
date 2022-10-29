from django.db import models
from accounts.models import User
# Create your models here.




class Website(models.Model):
    name =models.CharField( max_length=100,blank=True, null=True)
    title = models.CharField( max_length=300,blank=True, null=True)
    description = models.TextField( blank=True, null=True)
    favicon = models.ImageField( upload_to='website/images', blank=True, null=True)
    facebook = models.URLField( max_length=200, blank=True, null=True)
    linkedin = models.URLField( max_length=200, blank=True, null=True)
    twitter = models.URLField( max_length=200, blank=True, null=True)
    tiktok = models.URLField( max_length=200, blank=True, null=True)
    whatsapp = models.URLField( max_length=200, blank=True, null=True)
    github = models.URLField( max_length=200, blank=True, null=True)
    keywords = models.TextField( blank=True, null=True)
    author = models.ForeignKey( User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.title
    
    
    