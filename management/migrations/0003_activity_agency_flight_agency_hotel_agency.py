# Generated by Django 5.0.4 on 2024-04-10 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_remove_activity_package_remove_flight_package_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='agency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.agency'),
        ),
        migrations.AddField(
            model_name='flight',
            name='agency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.agency'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='agency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.agency'),
        ),
    ]
