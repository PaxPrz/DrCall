# Generated by Django 3.1 on 2020-09-02 15:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20200902_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 2, 20, 58, 20, 861365)),
        ),
    ]
