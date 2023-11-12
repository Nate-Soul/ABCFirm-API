# Generated by Django 4.2.7 on 2023-11-12 14:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('transcribeapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transcription',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='transcription',
            name='resource_name',
        ),
        migrations.AddField(
            model_name='transcription',
            name='resource_file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/', verbose_name='Resource'),
        ),
        migrations.AddField(
            model_name='transcription',
            name='web_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Resource Web ID'),
        ),
    ]
