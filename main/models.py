from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

# Create your models here.
class User(AbstractUser):
    dob = models.DateField(verbose_name="Date of Birth")
    location = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20)
    balance = models.FloatField(max_length=1000000)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)