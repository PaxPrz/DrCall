# Generated by Django 3.1 on 2020-08-28 16:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0011_auto_20200828_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 28, 23, 36, 54, 700837)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='link',
            field=models.CharField(default='no', max_length=800),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='prev_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 28, 22, 36, 54, 700907)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 28, 22, 36, 54, 700870)),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 28, 22, 36, 54, 701731)),
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 28, 22, 36, 54, 699366)),
        ),
    ]
