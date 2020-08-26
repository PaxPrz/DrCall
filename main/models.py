from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings
import os, datetime

def generate_upload_path(instance, filename):
    print("GENERATE UPLOAD PATH CALLED!")
    filename, ext = os.path.splitext(filename.lower())
    filename = "%s.%s%s" %(slugify(filename), datetime.datetime.now().strftime("%Y-%m-%d..%H-%M-%S"), ext)
    return '%s/%s' % (settings.PROFILE_UPLOAD_PATH, filename)

GENDER = (
    ('Male', 'MALE'),
    ('Female', 'FEMALE'),
    ('Other', 'OTHER'),
)

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=40)
    dob = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=20)
    balance = models.FloatField(max_length=1000000, default=100)
    contact = models.CharField(max_length=15, null=True)
    gender = models.CharField(choices=GENDER, max_length=50)
    profile_pic = models.ImageField(upload_to=generate_upload_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)
    
