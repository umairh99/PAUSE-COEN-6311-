# Generated by Django 5.0.4 on 2024-04-11 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0011_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='payment_info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
