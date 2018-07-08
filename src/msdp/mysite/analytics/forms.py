from django import forms
from .models import Analytics

class AnalyticsForm(forms.ModelForm):
    class Meta:
        model = Analytics
        #fields = ['TripId', 'DayOfService', 'ProgrNumber', 'StopPointId']
        fields = ['LineId', 'Month']
