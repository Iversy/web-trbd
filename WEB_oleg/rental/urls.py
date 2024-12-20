from django.urls import path
from .views import *

urlpatterns = [
    path('clients/', client_list, name='client_list'),
    path('clients/create/', client_create, name='client_create'),
    path('clients/update/<int:pk>/', client_update, name='client_update'),
    path('clients/delete/<int:pk>/', client_delete, name='client_delete'),
    path('rent/report/', rent_report, name='rent_report'),
    path('rent/report/csv/', rent_report_csv, name='rent_report_csv'),
    path('', home, name='home'),
    path('cars/', car_list, name='car_list'),
    path('cars/create/', car_create, name='car_create'),
    path('cars/update/<int:pk>/', car_update, name='car_update'),
    path('cars/delete/<int:pk>/', car_delete, name='car_delete'),

    path('services/', service_list, name='service_list'),
    path('services/create/', service_create, name='service_create'),
    path('services/update/<int:pk>/', service_update, name='service_update'),
    path('services/delete/<int:pk>/', service_delete, name='service_delete'),

    path('rents/', rent_list, name='rent_list'),
    path('rents/create/', rent_create, name='rent_create'),
    path('rents/update/<int:pk>/', rent_update, name='rent_update'),
    path('rents/delete/<int:pk>/', rent_delete, name='rent_delete'),

    path('maintenances/', maintenance_list, name='maintenance_list'),
    path('maintenances/create/', maintenance_create, name='maintenance_create'),
    path('maintenances/update/<int:pk>/', maintenance_update, name='maintenance_update'),
    path('maintenances/delete/<int:pk>/', maintenance_delete, name='maintenance_delete'),
    path('maintenances/report/',
         maintenance_report, name='maintenance_report'),
    path('maintenances/report/csv/',
         maintenance_report_csv, name='maintenance_report_csv'),

    
    path('clients/table/', client_table, name='client_table'),
    path('rents/table/', rent_table, name='rent_table'),
    path('services/table/', service_table, name='service_table'),
    path('cars/table/', car_table, name='car_table'),
    path('maintenances/table/', maintenance_table, name='maintenance_table'),
    path('megatable/', all_data_list, name='all_data_list'),
]

