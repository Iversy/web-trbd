from django.shortcuts import render, redirect
from .models import Client, Rent, Service, Maintenance, Car
from .forms import ClientForm, CarForm, ServiceForm, MaintenanceForm, RentForm
from .utils import get_all_urls



import csv
from django.http import HttpResponse


def home(request):
    return render(request, 'index.html')

def client_list(request):
    query = request.GET.get('q')  # Получаем параметр фильтрации из URL
    if query:
        clients = Client.objects.filter(name__icontains=query)  # Фильтруем по имени
    else:
        clients = Client.objects.all()  # Получаем всех клиентов
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

def rent_report(request):
    rents = Rent.objects.select_related('client', 'car')  # Получаем аренды с информацией о клиентах и автомобилях
    return render(request, 'rental/rent_report.html', {'rents': rents})


def rent_report_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rent_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Клиент', 'Автомобиль', 'Дата начала', 'Дата окончания', 'Цена'])

    rents = Rent.objects.select_related('client', 'car')
    for rent in rents:
        writer.writerow([rent.client.name, rent.car.model, rent.start, rent.end, rent.price])

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
