# Generated by Django 3.0.4 on 2020-04-02 13:38

import content.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_contents_lecture'),
    ]

    operations = [
        migrations.AddField(
            model_name='contents',
            name='preview',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contents',
            name='lecture',
            field=models.FileField(blank=True, null=True, upload_to=content.models.file_path),
        ),
    ]