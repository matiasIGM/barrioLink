# Generated by Django 4.2.5 on 2023-11-25 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_delete_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='capital_regional2',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
