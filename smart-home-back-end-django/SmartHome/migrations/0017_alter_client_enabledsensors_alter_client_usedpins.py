# Generated by Django 4.0.4 on 2022-08-16 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartHome', '0016_alter_client_enabledsensors_alter_client_usedpins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='enabledSensors',
            field=models.JSONField(default=list, max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='usedPins',
            field=models.JSONField(default=list, max_length=100),
        ),
    ]
