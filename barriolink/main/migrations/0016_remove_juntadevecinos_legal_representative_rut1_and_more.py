# Generated by Django 4.2.5 on 2023-11-13 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_juntadevecinos_legal_representative_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='juntadevecinos',
            name='legal_representative_rut1',
        ),
        migrations.RemoveField(
            model_name='residencecertificate',
            name='certificate_filename2',
        ),
    ]