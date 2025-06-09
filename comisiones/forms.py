from django import forms
from .models import Comision, Egresos

class ComisionForm(forms.ModelForm):
    class Meta:
        model = Comision
        fields = ['estado_vale_vista', 'valor_vale_vista']
        labels = {
            'estado_vale_vista': 'Estado de la Comisión',
            'valor_vale_vista': 'Valor de la Comisión',
        }
        widgets = {
            'estado_vale_vista': forms.Select(choices=Comision.ESTADO_VALE_VISTA_CHOICES, attrs={'class': 'form-select'}),
            'valor_vale_vista': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class EgresosForm(forms.ModelForm):
    class Meta:
        model = Egresos
        fields = ['descripcion', 'valor_egreso']
        labels = {
            'descripcion': 'Descripcion del egreso',
            'valor_egreso': 'Valor del egreso de dinero'
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Gasolina y comida en trayecto.'}),
            'valor_egreso': forms.NumberInput(attrs={'class': 'form-control','placeholder': '200000'}),
        }