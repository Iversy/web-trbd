from django.urls import path
from .views import client_list, client_create, client_update, client_delete

urlpatterns = [
    path('clients/', client_list, name='client_list'),
    path('clients/create/', client_create, name='client_create'),
    path('clients/update/<int:pk>/', client_update, name='client_update'),
    path('clients/delete/<int:pk>/', client_delete, name='client_delete'),
]
