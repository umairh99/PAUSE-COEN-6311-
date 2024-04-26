# Generated by Django 5.0.4 on 2024-04-10 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_activity_agency_flight_agency_hotel_agency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='pictures',
            field=models.ManyToManyField(blank=True, to='management.photo'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='pictures',
            field=models.ManyToManyField(blank=True, to='management.photo'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='pictures',
            field=models.ManyToManyField(blank=True, to='management.photo'),
        ),
    ]