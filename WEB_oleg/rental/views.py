import csv

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.db import models


from .forms import CarForm, ClientForm, MaintenanceForm, RentForm, ServiceForm
from .models import Car, Client, Maintenance, Rent, Service
from .utils import get_all_urls


import django_tables2 as tables
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_filters import FilterSet, CharFilter
from django_tables2.utils import A

import threading

def remove_contains_at_end(s):
    if s.endswith('__contains'):
        return s[:-len('__contains')]
    return s


def oleg_table(update, delete, _model):
    class SimpleTable(tables.Table):
        Изменить = tables.LinkColumn(update, text='Изменить', args=[A('pk')],
                                orderable=False, empty_values=())
        Удалить = tables.LinkColumn(delete, text='Удалить', args=[A('pk')],
                                orderable=False, empty_values=())

        class Meta:
            model = _model
    return SimpleTable


class RentFilter(FilterSet):
    client__name = CharFilter(lookup_expr='icontains', label="ФИО клиена")
    car__model = CharFilter(lookup_expr='icontains', label="Модель")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.filters:
            match field_name:
                case "client__name":
                    continue
                case "car__model":
                    continue
            self.filters[field_name].label = self.get_verbose_name(
                field_name)
    def get_verbose_name(self, field_name):
        print(field_name, remove_contains_at_end(field_name))
        field = self._meta.model._meta.get_field(remove_contains_at_end(field_name))
        return field.verbose_name.capitalize()

    class Meta:
        _model = Rent
        model = _model
        print(_model._meta.get_fields())
        fields = {
            name.name: ["contains"]
            for name in _model._meta.get_fields()
            if isinstance(name, (
                models.CharField,
                models.TextField,
                models.DateField,
                models.IntegerField,
                models.FloatField,
            ))
        }
        

class MaintenanceFilter(FilterSet):
    service__name = CharFilter(lookup_expr='icontains', label="Сервис")
    car__model = CharFilter(lookup_expr='icontains', label="Модель")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.filters:
            match field_name:
                case "service__name":
                    continue
                case "car__model":
                    continue
            self.filters[field_name].label = self.get_verbose_name(
                field_name)


    def get_verbose_name(self, field_name):
        print(field_name, remove_contains_at_end(field_name))
        field = self._meta.model._meta.get_field(
            remove_contains_at_end(field_name))
        return field.verbose_name.capitalize()
    
    class Meta:
        _model = Maintenance
        model = _model
        print(_model._meta.get_fields())
        fields = {
            name.name: ["contains"]
            for name in _model._meta.get_fields()
            if isinstance(name, (
                models.CharField,
                models.TextField,
                models.DateField,
                models.IntegerField,
                models.FloatField,
            ))
        }


def oleg_filter(_model):
    class ClientFilter(FilterSet):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name in self.filters:
                self.filters[field_name].label = self.get_verbose_name(
                    field_name)
        def get_verbose_name(self, field_name):
            print(field_name, remove_contains_at_end(field_name))
            field = self._meta.model._meta.get_field(remove_contains_at_end(field_name))
            return field.verbose_name.capitalize()

        class Meta:
            model = _model
            print(_model._meta.get_fields())
            fields = {
                name.name: ["contains"]
                for name in _model._meta.get_fields()
                if isinstance(name, (
                    models.CharField,
                    models.TextField,
                    models.DateField,
                    models.IntegerField,
                    models.FloatField,
                    # models.ForeignKey,
                ))
            }
    return ClientFilter

def oleg_table_view(update, delete, _model, filter=None):
    class FilteredPersonListView(SingleTableMixin, FilterView):
        table_class = oleg_table(update, delete, _model)
        model = _model
        template_name = "rental/oleg.html"

        filterset_class = filter or oleg_filter(_model)

        def get_context_data(self, *args, **kwargs):
            context = super().get_context_data(*args, **kwargs)
            # context['create_url'] = create
            return context
    return FilteredPersonListView



def client_table(request):
    query = request.GET.get('q') 
    if query:
        clients = Client.objects.filter(name__icontains=query)
    else:
        clients = Client.objects.all()
    context = {
        'clients': clients,
    }

    return render(request, 'all_data_list.html', context)
    
def car_table(request):
    query = request.GET.get('q') 
    if query:
        cars = Car.objects.filter(model__icontains=query)
    else:
        cars = Car.objects.all()
    context = {
        'cars': cars,
    }

    return render(request, 'all_data_list.html', context)
    
def rent_table(request):
    query = request.GET.get('q') 
    if query:
        rents = Rent.objects.filter(client__name__icontains=query)
    else:
        rents = Rent.objects.all()
    context = {
        'rents': rents,
    }

    return render(request, 'all_data_list.html', context)
    
def service_table(request):
    query = request.GET.get('q') 
    if query:
        services = Service.objects.filter(name__icontains=query)
    else:
        services = Service.objects.all()
    context = {
        'services': services,
    }

    return render(request, 'all_data_list.html', context)
    
def maintenance_table(request):
    query = request.GET.get('q') 
    if query:
        maintenances = Maintenance.objects.filter(car__model__icontains=query)
    else:
        maintenances = Maintenance.objects.all()

    maintenances = Maintenance.objects.all()
    context = {
        'maintenances': maintenances,
    }

    return render(request, 'all_data_list.html', context)
    



def all_data_list(request):
    query = request.GET.get('q') 
    if query:
        clients = Client.objects.filter(name__icontains=query)
        cars = Car.objects.filter(model__icontains=query)
        services = Service.objects.filter(name__icontains=query)
        rents = Rent.objects.filter(client__name__icontains=query)
        maintenances = Maintenance.objects.filter(car__model__icontains=query)
    else:
        clients = Client.objects.all()
        cars = Car.objects.all()
        services = Service.objects.all()
        rents = Rent.objects.all()
        maintenances = Maintenance.objects.all()
    
    context = {
        'clients': clients,
        'cars': cars,
        'services': services,
        'rents': rents,
        'maintenances': maintenances,
    }
    
    return render(request, 'all_data_list.html', context)


def home(request):
    return render(request, 'index.html')

def client_list(request):
    query = request.GET.get('q')  
    if query:
        clients = Client.objects.filter(name__icontains=query)
    else:
        clients = Client.objects.all()
    return render(request, 'rental/client_list.html', {'clients': clients})

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('client_list')  
    else:
        form = ClientForm()
    return render(request, 'rental/client_form.html', {'form': form})

def client_update(request, pk):
    client = Client.objects.get(pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()  
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'rental/client_form.html', {'form': form})

def client_delete(request, pk):
    client = Client.objects.get(pk=pk)
    if request.method == 'POST':
        client.delete()  
        return redirect('client_list')
    return render(request, 'rental/client_confirm_delete.html', {'client': client})


def car_report(request):
    cars_with_counts = Car.objects.annotate(
        rent_count=Count('rent'),
        maintenance_count=Count('maintenance')
    ).values('model', 'year', 'color', 'number', 'rent_count', 'maintenance_count')
    return render(request, 'rental/car_report.html', {'cars_with_counts': cars_with_counts})

import threading



def car_report_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="car_report.csv"'

    writer = csv.writer(response)
    def write(writer):
        writer.writerow(['Модель', 'Год', 'Цвет',
                        'Номер', 'Число аренд', 'Число обслуживаний'])

        cars_with_counts = Car.objects.annotate(
            rent_count=Count('rent'),
            maintenance_count=Count('maintenance')
        ).values('model', 'year', 'color', 'number', 'rent_count', 'maintenance_count')
        # print(type(cars_with_counts))
        # print(type(cars_with_counts[0]))
        for car in cars_with_counts:
            writer.writerow([
                car["model"],
                car["year"],
                car["color"],
                car["number"],
                car["rent_count"],
                car["maintenance_count"],
                ])
    thread = threading.Thread(target=write, args=(writer,))
    thread.start()
    thread.join()

    return response


def maintenance_report(request):
    # Получаем обслуживания с информацией о сервисе и автомобилях
    maintenances = Maintenance.objects.select_related('service', 'car')
    return render(request, 'rental/maintenance_report.html', {'maintenances': maintenances})


def maintenance_report_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="maintenance_report.csv"'

    writer = csv.writer(response)
    def write(writer):
        writer.writerow(['Автомобиль', 'Сервис', 'Дата начала',
                        'Дата окончания', 'Цена'])

        maintances = Maintenance.objects.select_related('car', 'service')
        for maintance in maintances:
            writer.writerow([maintance.car.model, maintance.service.name, maintance.start, maintance.end, maintance.price])

    thread = threading.Thread(target=write, args=(writer,))
    thread.start()
    thread.join()

    return response

def rent_report(request):
    rents = Rent.objects.select_related('client', 'car')  # Получаем аренды с информацией о клиентах и автомобилях
    return render(request, 'rental/rent_report.html', {'rents': rents})


def rent_report_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rent_report.csv"' 

    writer = csv.writer(response)
    def write(writer):
        writer.writerow(['Клиент', 'Автомобиль', 'Дата начала', 'Дата окончания', 'Цена'])

        rents = Rent.objects.select_related('client', 'car')
        for rent in rents:
            writer.writerow([rent.client.name, rent.car.model, rent.start, rent.end, rent.price])
    thread = threading.Thread(target=write, args=(writer,))
    thread.start()
    thread.join()
    return response

def car_list(request):
    query = request.GET.get('q')
    if query:
        cars = Car.objects.filter(model__icontains=query)
    else:
        cars = Car.objects.all()
    return render(request, 'rental/car_list.html', {'cars': cars})

def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'rental/car_form.html', {'form': form})

def car_update(request, pk):
    car = Car.objects.get(pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm(instance=car)
    return render(request, 'rental/car_form.html', {'form': form})

def car_delete(request, pk):
    car = Car.objects.get(pk=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')
    return render(request, 'rental/car_confirm_delete.html', {'car': car})

def service_list(request):
    query = request.GET.get('q')
    if query:
        services = Service.objects.filter(name__icontains=query)
    else:
        services = Service.objects.all()
    return render(request, 'rental/service_list.html', {'services': services})

def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'rental/service_form.html', {'form': form})

def service_update(request, pk):
    service = Service.objects.get(pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'rental/service_form.html', {'form': form})

def service_delete(request, pk):
    service = Service.objects.get(pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'rental/service_confirm_delete.html', {'service': service})

def rent_list(request):
    query = request.GET.get('q')
    if query:
        rents = Rent.objects.filter(client__name__icontains=query)
    else:
        rents = Rent.objects.all()
    return render(request, 'rental/rent_list.html', {'rents': rents})

def rent_create(request):
    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rent_list')
    else:
        form = RentForm()
    return render(request, 'rental/rent_form.html', {'form': form})

def rent_update(request, pk):
    rent = Rent.objects.get(pk=pk)
    if request.method == 'POST':
        form = RentForm(request.POST, instance=rent)
        if form.is_valid():
            form.save()
            return redirect('rent_list')
    else:
        form = RentForm(instance=rent)
    return render(request, 'rental/rent_form.html', {'form': form})

def rent_delete(request, pk):
    rent = Rent.objects.get(pk=pk)
    if request.method == 'POST':
        rent.delete()
        return redirect('rent_list')
    return render(request, 'rental/rent_confirm_delete.html', {'rent': rent})

def maintenance_list(request):
    query = request.GET.get('q')
    if query:
        maintenances = Maintenance.objects.filter(car__model__icontains=query)
    else:
        maintenances = Maintenance.objects.all()
    return render(request, 'rental/maintenance_list.html', {'maintenances': maintenances})

def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm()
    return render(request, 'rental/maintenance_form.html', {'form': form})



def maintenance_update(request, pk):
    maintenance = Maintenance.objects.get(pk=pk)
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm(instance=maintenance)
    return render(request, 'rental/maintenance_form.html', {'form': form})

def maintenance_delete(request, pk):
    maintenance = Maintenance.objects.get(pk=pk)
    if request.method == 'POST':
        maintenance.delete()
        return redirect('maintenance_list')
    return render(request, 'rental/maintenance_confirm_delete.html', {'maintenance': maintenance})
