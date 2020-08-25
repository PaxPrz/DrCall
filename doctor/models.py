from django.db import models
from main.models import User
# from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    contact = models.CharField(max_length=15)
    speciality = models.ManyToManyField('Specialities')
    education = models.ManyToManyField('Education')
    hospital = models.ManyToManyField('Hospital')

    def __str__(self):
        return '(D):'+self.user.username

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