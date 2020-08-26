# Generated by Django 3.1 on 2020-08-25 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_doctor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='contact',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='education',
            field=models.ManyToManyField(blank=True, null=True, to='doctor.Education'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='hospital',
            field=models.ManyToManyField(blank=True, null=True, to='doctor.Hospital'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='speciality',
            field=models.ManyToManyField(blank=True, null=True, to='doctor.Specialities'),
        ),
    ]