from django import forms
from .models import Client, Car, Service, Rent, Maintenance
from django.utils import timezone

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'birthday': DateInput(),
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = '__all__'
        widgets = {
            'start': DateTimeInput(),
            'end': DateTimeInput(),
        }
    def __init__(self, *args, **kwargs):
        super(RentForm, self).__init__(*args, **kwargs)
        self.fields['start'].initial = timezone.now()  
        self.fields['end'].initial = timezone.now()    


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'
        widgets = {
            'start': DateTimeInput(),
            'end': DateTimeInput(),
        }

    def __init__(self, *args, **kwargs):
        super(MaintenanceForm, self).__init__(*args, **kwargs)
        self.fields['start'].initial = timezone.now()  
        self.fields['end'].initial = timezone.now()    
