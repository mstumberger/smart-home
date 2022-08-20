# Generated by Django 4.0.4 on 2022-08-14 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SmartHome', '0010_alter_client_availablegpiopins_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Sensor',
            new_name='Module',
        ),
        migrations.RenameField(
            model_name='gpiopinconfig',
            old_name='sensor',
            new_name='module',
        ),
        migrations.RemoveField(
            model_name='dashboard',
            name='sensor_id',
        ),
        migrations.RemoveField(
            model_name='gpiopinconfig',
            name='pins',
        ),
        migrations.AddField(
            model_name='dashboard',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SmartHome.module'),
        ),
        migrations.AddField(
            model_name='gpiopinconfig',
            name='gpioPin',
            field=models.IntegerField(max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='gpiopinconfig',
            name='pin',
            field=models.IntegerField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='enabledSensors',
            field=models.JSONField(default=[], max_length=100),
        ),
    ]
