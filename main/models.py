from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings
import os, datetime

def generate_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename.lower())
    filename = "%s.%s%s" %(slugify(filename), datetime.datetime.now().strftime("%Y-%m-%d..%H-%M-%S"), ext)
    return '%s/%s' % (settings.PROFILE_UPLOAD_PATH, filename)

# Create your models here.
class User(AbstractUser):
    dob = models.DateField(verbose_name="Date of Birth")
    location = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20)
    balance = models.FloatField(max_length=1000000)
    profile_pic = models.ImageField(upload_to=generate_upload_path)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)
    
