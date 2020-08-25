from django.db import models
from main.models import User
from patient.models import Patient
from django.contrib.postgres.fields import ArrayField
import os
from settings import PROFILE_UPLOAD_PATH
import datetime

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    contact = models.IntegerField(max_length=10)
    rating = models.ManyToManyField(Rating)
    speciality = models.ManyToManyField(Specialities)
    education = models.ManyToManyField(Education)
    hospital = models.ManyToManyField(Hospital)
    profile_pic = models.ImageField(upload_to=generate_upload_path)

    def __str__(self):
        return self.user.username

    def generate_upload_path(self, filename):
        filename, ext = os.path.splitext(filename.lower())
        filename = "%s.%s%s" %(slugify(filename), datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S"), ext)
        return '%s/%s' % (PROFILE_UPLOAD_PATH, filename)

class Rating(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rating = models.IntegerField(max_length=10)

    def __str__(self):
        return str(self.rating)

class Specialities(models.Model):
    speciality = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.speciality

class Education(models.Model):
    education = models.CharField(max_length=20)

    def __str__(self):
        return self.education

class Hospital(models.Model):
    hospital = models.CharField(max_length=50)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.hospital