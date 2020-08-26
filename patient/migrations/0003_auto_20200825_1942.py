# Generated by Django 3.1 on 2020-08-25 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0004_auto_20200825_1942'),
        ('patient', '0002_auto_20200825_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='allowed_doctor',
            field=models.ManyToManyField(to='doctor.Doctor'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='rating',
            field=models.ManyToManyField(to='patient.Rating'),
        ),
    ]