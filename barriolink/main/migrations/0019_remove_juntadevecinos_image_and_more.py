# Generated by Django 4.2.5 on 2023-11-16 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_juntadevecinos_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='juntadevecinos',
            name='image',
        ),
        migrations.AddField(
            model_name='juntadevecinos',
            name='signatue_img',
            field=models.ImageField(default=0, upload_to='uploads/signatures/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='juntadevecinos',
            name='logo_symbol',
            field=models.ImageField(default=0, upload_to='uploads/logos/'),
            preserve_default=False,
        ),
    ]