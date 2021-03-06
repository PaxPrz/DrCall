# Generated by Django 3.1 on 2020-08-28 15:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0009_auto_20200827_1655'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ['-appointment_time']},
        ),
        migrations.AlterModelOptions(
            name='medicine',
            options={'ordering': ['-prescription__date']},
        ),
        migrations.AlterModelOptions(
            name='prescription',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='appointment',
            name='link',
            field=models.CharField(default='no', max_length=200),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 28, 22, 12, 0, 209298)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='prev_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 28, 21, 12, 0, 209361)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 28, 21, 12, 0, 209328)),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 28, 21, 12, 0, 210877)),
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 28, 21, 12, 0, 207737)),
        ),
    ]
