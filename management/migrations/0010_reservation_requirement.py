# Generated by Django 4.2.1 on 2023-07-18 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_reservation_viewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='requirement',
            field=models.TextField(blank=True, default=''),
        ),
    ]
