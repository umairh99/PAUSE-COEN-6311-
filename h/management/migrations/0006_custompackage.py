# Generated by Django 5.0.4 on 2024-04-11 16:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_alter_package_activities_alter_package_flights_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activities', models.ManyToManyField(to='management.activity')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('flights', models.ManyToManyField(to='management.flight')),
                ('hotels', models.ManyToManyField(to='management.hotel')),
            ],
        ),
    ]