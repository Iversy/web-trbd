# Generated by Django 5.1.4 on 2024-12-21 18:09

import django.db.models.deletion
import rental.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0002_alter_car_number_alter_car_year_alter_client_license_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='color',
            field=models.CharField(max_length=50, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='car',
            name='model',
            field=models.CharField(max_length=255, verbose_name='Модель'),
        ),
        migrations.AlterField(
            model_name='car',
            name='number',
            field=models.CharField(max_length=20, validators=[rental.models.validate_number_plate], verbose_name='Госномер'),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.IntegerField(validators=[rental.models.validate_year], verbose_name='Год выпуска'),
        ),
        migrations.AlterField(
            model_name='client',
            name='birthday',
            field=models.DateField(verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='client',
            name='license',
            field=models.CharField(max_length=255, validators=[rental.models.validate_license], verbose_name='Права'),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=255, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=20, validators=[rental.models.validate_ru_phone_number], verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rental.car', verbose_name='Машина'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='end',
            field=models.DateTimeField(verbose_name='Конец'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='price',
            field=models.FloatField(validators=[rental.models.validate_price], verbose_name='Стоимость'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rental.service', verbose_name='Сервис'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='start',
            field=models.DateTimeField(verbose_name='Начало'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rental.car', verbose_name='Машина'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rental.client', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='end',
            field=models.DateTimeField(verbose_name='Конец'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='price',
            field=models.FloatField(validators=[rental.models.validate_price], verbose_name='Стоимость'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='start',
            field=models.DateTimeField(verbose_name='Начало'),
        ),
        migrations.AlterField(
            model_name='service',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='service',
            name='payment_details',
            field=models.TextField(verbose_name='Реквизиты'),
        ),
    ]
