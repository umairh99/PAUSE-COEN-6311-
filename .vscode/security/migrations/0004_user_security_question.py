# Generated by Django 5.0.4 on 2024-04-13 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0003_user_is_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='security_question',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]