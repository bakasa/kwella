# Generated by Django 3.1.7 on 2021-04-13 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_user_otp'),
        ('trips', '0002_auto_20210411_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trips_as_driver', to='users.driver', verbose_name='Trip Driver'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='rider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trips_as_rider', to='users.rider', verbose_name='Trip Rider'),
        ),
    ]
