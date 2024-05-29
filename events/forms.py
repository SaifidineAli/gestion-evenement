from django import forms
from .models import Event, Registration

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        #fields = ['title', 'description', 'date', 'organizer']
        fields = ['title', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = []
