# Generated by Django 3.1 on 2020-08-28 16:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20200828_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 28, 22, 36, 54, 695901)),
        ),
    ]
