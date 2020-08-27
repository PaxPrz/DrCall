# Generated by Django 3.1 on 2020-08-27 10:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_auto_20200827_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 27, 16, 51, 37, 390013)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='prev_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 27, 15, 51, 37, 390071)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 27, 15, 51, 37, 390041)),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 27, 15, 51, 37, 390650)),
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 27, 15, 51, 37, 388833)),
        ),
    ]