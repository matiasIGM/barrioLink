# Generated by Django 4.2.5 on 2023-12-03 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0003_rename_community_space_events_community_spacea'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservationmember',
            name='is_validated',
            field=models.BooleanField(default=False),
        ),
    ]