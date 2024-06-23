from django import forms
from django.forms import ModelForm, TextInput, Textarea
from .models import  Financeiro

class FinanceiroForm(forms.ModelForm):
    class Meta:
        model = Financeiro
        exclude = ()
        fields = '__all__'
        widgets = {
                    'fazenda': forms.Select(attrs={'class': 'form-control', 'id':'validationTooltip01'}),

                    }
