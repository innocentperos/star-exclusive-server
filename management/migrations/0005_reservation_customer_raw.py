# Generated by Django 4.2.1 on 2023-06-28 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_reservation_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='customer_raw',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
