from django import forms
from .models import *
class HumanForm(forms.ModelForm):
    class Meta:
        model = Human
        fields=(
            'name',
        )	
