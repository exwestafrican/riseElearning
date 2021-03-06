# Generated by Django 3.0.4 on 2020-05-07 09:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_auto_20200507_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='membership_end_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='membership_start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
