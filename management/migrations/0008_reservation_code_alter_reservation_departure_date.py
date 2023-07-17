# Generated by Django 4.2.1 on 2023-07-17 12:28

from django.db import migrations, models
import management.models


class Migration(migrations.Migration):
    dependencies = [
        ("management", "0007_alter_reservation_departure_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="code",
            field=models.CharField(
                blank=True,
                default=management.models.generate_reservation_code,
                max_length=50,
                unique=False,
                null = True
            ),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="departure_date",
            field=models.DateTimeField(),
        ),
    ]
