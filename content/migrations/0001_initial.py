# Generated by Django 3.0.4 on 2020-03-26 09:18

import content.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('title', models.CharField(max_length=150)),
                ('lesson_type', models.CharField(choices=[('video', 'Video'), ('slide', 'Slide'), ('excersise', 'Excerise'), ('notes', 'Notes')], default='video', max_length=100)),
                ('embeded_content', models.CharField(blank=True, max_length=210, null=True)),
                ('last_saved', models.DateTimeField(auto_now=True)),
                ('order', content.fields.PositionField(default=-1)),
                ('chapter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.Chapter')),
            ],
            options={
                'verbose_name': 'Content',
                'verbose_name_plural': 'Contents',
                'db_table': '',
                'ordering': ['order'],
                'managed': True,
            },
        ),
        migrations.AddConstraint(
            model_name='contents',
            constraint=models.UniqueConstraint(fields=('chapter', 'title'), name='unique_lesson'),
        ),
    ]
