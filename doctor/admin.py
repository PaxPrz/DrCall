from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Doctor)
admin.site.register(models.Education)
admin.site.register(models.Hospital)
admin.site.register(models.Specialities)