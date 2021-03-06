from django.db import models
from django.contrib.auth.models import User

#Importing date method
import datetime

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to ='media/Profile/',null=True)
    bio = models.CharField(max_length=350)

    '''Method to filter database results'''
    def __str__(self):
        return self.user


class Post(models.Model):

    post_image = models.ImageField(upload_to ='media/Posts')
    post_caption = models.CharField(max_length=700)
    post_user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True, null = True)

class Comment(models.Model):

    comment = models.CharField(max_length=350)
    post = models.ForeignKey('Post',on_delete=models.CASCADE)
    user = models.ForeignKey('Profile',on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user