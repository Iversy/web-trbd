# Generated by Django 5.1.4 on 2024-12-21 09:20

import rental.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='number',
            field=models.CharField(max_length=20, validators=[rental.models.validate_number_plate]),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.IntegerField(validators=[rental.models.validate_year]),
        ),
        migrations.AlterField(
            model_name='client',
            name='license',
            field=models.CharField(max_length=255, validators=[rental.models.validate_license]),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=20, validators=[rental.models.validate_ru_phone_number]),
        ),
    ]
