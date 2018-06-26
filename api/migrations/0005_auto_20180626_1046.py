# Generated by Django 2.0.6 on 2018-06-26 10:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0004_event_createdby'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='forGroups',
            new_name='audience',
        ),
        migrations.RemoveField(
            model_name='event',
            name='helpers',
        ),
        migrations.AddField(
            model_name='event',
            name='helpers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
