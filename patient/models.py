from django.db import models
from django.conf import settings
from main.models import User
import datetime
import os
from django.utils.text import slugify

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    allowed_doctor = models.ManyToManyField('doctor.Doctor')
    rating = models.ManyToManyField('Rating') 

    def __str__(self):
        return '(P)'+self.user.username

class Rating(models.Model):
    doctor = models.ForeignKey('doctor.Doctor', on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return self.doctor.user.username+str(self.rating)

def generate_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename.lower())
    filename = "%s.%s%s" %(slugify(filename), datetime.datetime.now().strftime("%Y-%m-%d..%H-%M-%S"), ext)
    return '%s/%s' % (settings.REPORT_IMAGE_PATH, filename)

class Report(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    date = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    institute = models.CharField(max_length=50, blank=True, null=True)
    added_by = models.ForeignKey('doctor.Doctor', null=True, on_delete=models.SET_NULL)
    content = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to=generate_upload_path, blank=True, null=True)

    def __str__(self):
        return self.title

class ReportImage(models.Model):
    report = models.ForeignKey('Report', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generate_upload_path)

    def __str__(self):
        return '(I):'+self.report.title

class Appointment(models.Model):
    patient = models.ForeignKey('Patient', null=True, on_delete=models.SET_NULL)
    problem = models.CharField(max_length=200)
    doctor = models.ForeignKey('doctor.Doctor', null=True, on_delete=models.SET_NULL)
    appointment_time = models.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(hours=1))
    time = models.DateTimeField(default=datetime.datetime.now())
    accepted = models.BooleanField(default=False)
    prev_time = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return '(A):'+self.time.strftime("%m-%d:%H-%M")
    
class Prescription(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctor.Doctor', null=True, on_delete=models.SET_NULL)
    diagnosis = models.CharField(max_length=50)
    date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.diagnosis

class Medicine(models.Model):
    primary = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100)
    dose = models.CharField(max_length=50, blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE)

    def __str__(self):
        return self.name