# Generated by Django 5.0.4 on 2024-04-09 13:07

import django.core.validators
import security.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(max_length=15, verbose_name='phone number')),
                ('picture', models.ImageField(blank=True, upload_to=security.models.picture_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'], message='Upload an image file (JPG, JPEG, PNG, GIF) only.')], verbose_name='profile picture')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='last name')),
                ('gender', models.CharField(blank=True, choices=[('p_n_t_s', 'Prefer not to say'), ('m', 'Male'), ('f', 'Female'), ('o', 'Others')], default='p_n_t_s', max_length=15, null=True, verbose_name='gender')),
                ('pincode', models.CharField(blank=True, max_length=6, null=True, verbose_name='pincode')),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, verbose_name='active status')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]