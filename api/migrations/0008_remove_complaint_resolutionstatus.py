# Generated by Django 2.0.6 on 2018-07-05 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20180705_2258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='resolutionStatus',
        ),
    ]