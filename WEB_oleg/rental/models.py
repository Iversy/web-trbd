import re
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

def validate_price(value):
    if value < 0:
        raise ValidationError('В минус не работаем, цена только положительная.')

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
    name = models.CharField(max_length=255)
    license = models.CharField(max_length=255, validators=[validate_license])
    birthday = models.DateField()
    phone = models.CharField(max_length=20, validators=[validate_ru_phone_number])
    def __str__(self):
        return self.name
    def clean(self):
        super().clean()
        if self.start > timezone.now():
            raise ValidationError('Привет человек из будущего!')
class Car(models.Model):
    model = models.CharField(max_length=255)
    year = models.IntegerField(validators=[validate_year])
    color = models.CharField(max_length=50)
    number = models.CharField(max_length=20, validators=[validate_number_plate])
    def __str__(self):
        return self.model

class Service(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    payment_details = models.TextField()
    def __str__(self):
        return self.name

class Rent(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)  
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)          
    start = models.DateTimeField()
    end = models.DateTimeField()
    price = models.FloatField(validators=[validate_price])

    def clean(self):
        super().clean()
        if self.start > self.end:
            raise ValidationError('Дата начала аренды должна быть меньше или равна дате окончания.')
        if self.start > timezone.now() or self.end > timezone.now():
            raise ValidationError('Даты начала и окончания аренды не должны быть в будущем.')

class Maintenance(models.Model):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)          
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)  
    start = models.DateTimeField()
    end = models.DateTimeField()
    price = models.FloatField(validators=[validate_price])

    def clean(self):
        super().clean()
        if self.start > self.end:
            raise ValidationError('Дата начала обслуживания должна быть меньше или равна дате окончания.')
        if self.start > timezone.now() or self.end > timezone.now():
            raise ValidationError('Даты начала и окончания обслуживания не должны быть в будущем.')
