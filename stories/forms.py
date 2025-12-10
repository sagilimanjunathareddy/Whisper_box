# stories/forms.py
from django import forms
from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'description', 'category', 'city', 'location', 'story_date']
        widgets = {
            'story_date': forms.DateInput(attrs={'type': 'date'}),
            'location': forms.TextInput(attrs={'placeholder': 'lat,lng  OR  leave blank and fill city'}),
            'city': forms.TextInput(attrs={'placeholder': 'City or place name (e.g., Chennai)'}),
        }
