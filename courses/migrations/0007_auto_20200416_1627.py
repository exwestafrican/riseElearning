# Generated by Django 3.0.4 on 2020-04-16 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_chapter_preivew'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='membership_required',
        ),
        migrations.RemoveField(
            model_name='course',
            name='price',
        ),
        migrations.AlterField(
            model_name='course',
            name='free',
            field=models.BooleanField(default=False),
        ),
    ]