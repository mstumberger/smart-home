# Generated by Django 4.0.4 on 2022-08-16 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartHome', '0014_alter_gpiopinconfig_gpiopin_alter_gpiopinconfig_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='enabledSensors',
            field=models.JSONField(default={}, max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='usedPins',
            field=models.JSONField(default={}, max_length=100),
        ),
    ]