# Generated by Django 3.0.4 on 2020-04-27 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_auto_20200413_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='contents',
            name='share_message',
            field=models.CharField(default='Learn more with Rise Elearning', max_length=150),
        ),
    ]
