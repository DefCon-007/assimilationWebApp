# Generated by Django 2.0.6 on 2018-07-09 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20180709_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='event',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='complaintEvent', to='api.event'),
        ),
    ]