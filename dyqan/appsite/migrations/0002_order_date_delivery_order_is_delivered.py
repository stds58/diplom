# Generated by Django 4.2.13 on 2024-06-23 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appsite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_delivery',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
    ]