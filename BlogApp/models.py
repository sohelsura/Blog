from django.db import models


# Create your models here.
class ContactMessages(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=255)


class UsersRegistered(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=30)
    # image = models.ImageField(upload_to="userimage", null=True, blank=True)
    active = models.BooleanField(default=True)

class BlogData(models.Model):
    image = models.ImageField(upload_to="blogimages", null=True, blank=True)
    title = models.CharField(max_length=255)
    smalldesc = models.CharField(max_length=500)
    maincontent = models.CharField(max_length=4000)
    datetime = models.DateTimeField(auto_now_add = True)
