# Generated by Django 3.1 on 2020-09-02 14:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0012_auto_20200828_2236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patient',
            options={'permissions': [('isPatient', 'Can open patient tabs')]},
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 2, 21, 23, 26, 428224)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='prev_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 2, 20, 23, 26, 428313)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 2, 20, 23, 26, 428268)),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 2, 20, 23, 26, 429358)),
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 9, 2, 20, 23, 26, 426111)),
        ),
    ]