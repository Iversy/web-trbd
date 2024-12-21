import re
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    if value < 1672:
        raise ValidationError('В 1672 году Фердинанд Вербист придумал первую миниатюрную модель самодвижущейся повозки с использованием парового котла. Это изобретение было создано как игрушка для китайского императора и не было предназначено для перевозки водителя или пассажира, но, вероятно, оно является первой самодвижущейся паровой машиной. А вы указали год до этого...')
    if value > timezone.now().year:
        raise ValidationError('Год не может быть позже текущего.')

def validate_number_plate(value):
    pattern = r'^[АВЕКМНОРСТУХ]{1} \d{3} [АВЕКМНОРСТУХ]{2} \d{2,3}$'
    if not re.match(pattern, value):
        raise ValidationError('Неправильный формат номера. Формат: "A 123 AB 12" или "A 123 AB 123".')



def validate_ru_phone_number(value):
    pattern = r'^\+7 \d{3} \d{3}-\d{2}-\d{2}$'
    if not re.match(pattern, value):
        raise ValidationError('Неправильный формат номера. Формат: "+7 123 456-78-90".')
def validate_license(value):
    pattern = r'^\d{2} \d{2} \d{6}$'
    if not re.match(pattern, value):
        raise ValidationError('Неправильный формат лицензии. Формат: "12 34 567890".')


class Client(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="ФИО")
    license = models.CharField(max_length=255,
                               verbose_name="Права",
                               validators=[validate_license])
    birthday = models.DateField(verbose_name="Дата рождения")
    phone = models.CharField(max_length=20,
                             verbose_name="Телефон",
                             validators=[validate_ru_phone_number])
    def __str__(self):
        return self.name

class Car(models.Model):
    model = models.CharField(max_length=255,
                             verbose_name="Модель",)
    year = models.IntegerField(validators=[validate_year],
                               verbose_name="Год выпуска",)
    color = models.CharField(max_length=50,
                             verbose_name="Цвет",)
    number = models.CharField(max_length=20,
                              verbose_name="Госномер",
                              validators=[validate_number_plate])
    def __str__(self):
        return self.model

class Service(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="Название",)
    address = models.CharField(max_length=255,
                               verbose_name="Адрес",)
    payment_details = models.TextField(verbose_name="Реквизиты")
    def __str__(self):
        return self.name

class Rent(models.Model):
    client = models.ForeignKey(Client, 
                               on_delete=models.SET_NULL, 
                               null=True,
                               verbose_name="Клиент",)
    car = models.ForeignKey(Car, 
                            on_delete=models.SET_NULL, 
                            null=True,
                            verbose_name="Машина",)
    start = models.DateTimeField(verbose_name="Начало")
    end = models.DateTimeField(verbose_name="Конец")
    price = models.FloatField(verbose_name="Стоимость")

    def clean(self):
        super().clean()
        if self.start > self.end:
            raise ValidationError('Дата начала аренды должна быть меньше или равна дате окончания.')
        if self.start > timezone.now() or self.end > timezone.now():
            raise ValidationError('Даты начала и окончания аренды не должны быть в будущем.')


class Maintenance(models.Model):
    car = models.ForeignKey(Car,
                            on_delete=models.SET_NULL,
                            null=True,
                            verbose_name="Машина",)
    service = models.ForeignKey(Service, 
                                on_delete=models.SET_NULL, 
                                null=True,
                                verbose_name="Сервис",)
    start = models.DateTimeField(verbose_name="Начало")
    end = models.DateTimeField(verbose_name="Конец")
    price = models.FloatField(verbose_name="Стоимость")

    def clean(self):
        super().clean()
        if self.start > self.end:
            raise ValidationError('Дата начала обслуживания должна быть меньше или равна дате окончания.')
        if self.start > timezone.now() or self.end > timezone.now():
            raise ValidationError('Даты начала и окончания обслуживания не должны быть в будущем.')
