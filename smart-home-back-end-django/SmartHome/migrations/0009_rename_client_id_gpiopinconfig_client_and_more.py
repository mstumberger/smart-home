# Generated by Django 4.0.4 on 2022-08-14 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SmartHome', '0008_sensor_client'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gpiopinconfig',
            old_name='client_id',
            new_name='client',
        ),
        migrations.RenameField(
            model_name='gpiopinconfig',
            old_name='sensor_id',
            new_name='sensor',
        ),
    ]