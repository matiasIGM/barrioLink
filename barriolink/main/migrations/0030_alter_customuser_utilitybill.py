# Generated by Django 4.2.5 on 2023-12-02 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_customuser_utilitybill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='utilityBill',
            field=models.FileField(blank=True, null=True, upload_to='uploads/utilityBills/'),
        ),
    ]