# Generated by Django 3.1 on 2020-08-26 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200825_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contact',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]