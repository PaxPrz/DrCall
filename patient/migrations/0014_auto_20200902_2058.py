# Generated by Django 3.1 on 2020-09-02 15:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0013_auto_20200902_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 2, 21, 58, 20, 873331)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='prev_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 2, 20, 58, 20, 873545)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 2, 20, 58, 20, 873435)),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 2, 20, 58, 20, 874990)),
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 9, 2, 20, 58, 20, 870505)),
        ),
    ]