from django import forms
from .models import Appartment

class AvailabilityForm(forms.Form):

    # appart_list =forms.ModelChoiceField(queryset=Appartment.objects.all(),empty_label="select_appartement")
    check_in = forms.DateTimeField(required=True,input_formats=['%Y-%m-%d %H:%M'],widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    check_out = forms.DateTimeField(required=True,input_formats=["%Y-%m-%d %H:%M"],widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
