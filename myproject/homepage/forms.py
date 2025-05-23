# feedback/forms.py
from django import forms
from .models import Feedback
import csv
from django.conf import settings
import os

class FeedbackForm(forms.ModelForm):
    station_name = forms.ChoiceField(choices=[], widget=forms.Select)
    crowded_level = forms.ChoiceField(choices=Feedback.CROWDED_CHOICES, widget=forms.Select)

    class Meta:
        model = Feedback
        fields = ['name','station_name', 'crowded_level', 'message']  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        station_choices = []
        csv_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'station_20.csv')
        
        if os.path.exists(csv_path):
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                station_choices = [(row['Station name'], row['Station name']) for row in reader]
        
        self.fields['station_name'].choices = station_choices
