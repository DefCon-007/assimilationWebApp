# Generated by Django 2.0.6 on 2018-07-05 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_complaint_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='created_at',
        ),
        migrations.AddField(
            model_name='complaint',
            name='resolutionStatus',
            field=models.NullBooleanField(),
        ),
    ]
