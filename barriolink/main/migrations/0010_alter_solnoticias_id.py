# Generated by Django 4.2.5 on 2023-11-12 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_publicacion_solnoticias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solnoticias',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
