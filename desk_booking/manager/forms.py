from django import forms
from .models import Floor
class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = ('name', 'map')