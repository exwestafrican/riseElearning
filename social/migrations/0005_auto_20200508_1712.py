# Generated by Django 3.0.4 on 2020-05-08 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_auto_20200507_0957'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='discription',
            new_name='bio',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='membership_end_date',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='membership_start_date',
        ),
    ]
