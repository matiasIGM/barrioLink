# Generated by Django 4.2.5 on 2023-12-03 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0004_reservation_is_validated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reservation_status',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
