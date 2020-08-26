from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Patient)
admin.site.register(models.Rating)
admin.site.register(models.Report)
admin.site.register(models.ReportImage)
admin.site.register(models.Appointment)
admin.site.register(models.Prescription)
admin.site.register(models.Medicine)
