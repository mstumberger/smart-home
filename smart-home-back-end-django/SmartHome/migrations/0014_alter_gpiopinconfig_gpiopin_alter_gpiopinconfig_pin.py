# Generated by Django 4.0.4 on 2022-08-16 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartHome', '0013_remove_gpiopinconfig_module_module_used_pins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpiopinconfig',
            name='gpioPin',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='gpiopinconfig',
            name='pin',
            field=models.IntegerField(null=True),
        ),
    ]
