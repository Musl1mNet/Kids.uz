# Generated by Django 4.2.1 on 2023-05-28 07:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_post_is_date_post_is_library_post_is_video_or_audio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_library',
        ),
        migrations.RemoveField(
            model_name='post',
            name='is_video_or_audio',
        ),
        migrations.AddField(
            model_name='post',
            name='is_audio',
            field=models.BooleanField(default=False, verbose_name='Audio'),
        ),
        migrations.AddField(
            model_name='post',
            name='is_video',
            field=models.BooleanField(default=False, verbose_name='Video'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Sana'),
        ),
    ]
