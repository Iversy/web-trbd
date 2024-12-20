from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255)
    license = models.CharField(max_length=255)
    birthday = models.DateField()
    phone = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Car(models.Model):
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    color = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
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
    price = models.FloatField()

class Maintenance(models.Model):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)          
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)  
    start = models.DateTimeField()
    end = models.DateTimeField()
    price = models.FloatField()
