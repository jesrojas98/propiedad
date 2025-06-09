from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = [
            'id_propiedad',
            'descripcion',
            'valor',
            'tipo_publicacion',
            'tipo_valor',
            'tipo_negocio',
            'fecha_expiracion',
            'comision_estimada',
            'destacada',
            'estado'
        ]
        widgets = {
            'fecha_expiracion': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


    def clean_valor(self):
        """Validar que el valor sea mayor a 0."""
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor <= 0:
            raise ValidationError("El valor debe ser mayor a 0.")
        return valor

    def clean_tipo_publicacion(self):
        """Validar que el tipo de publicación sea válido."""
        tipo_publicacion = self.cleaned_data.get('tipo_publicacion')
        tipos_validos = [choice[0] for choice in Publicacion.TIPO_PUBLICACION_CHOICES]
        if tipo_publicacion not in tipos_validos:
            raise ValidationError("El tipo de publicación no es válido.")
        return tipo_publicacion

    def clean_tipo_valor(self):
        """Validar que el tipo de valor sea válido."""
        tipo_valor = self.cleaned_data.get('tipo_valor')
        tipos_validos = [choice[0] for choice in Publicacion.TIPO_VALOR_CHOICES]
        if tipo_valor not in tipos_validos:
            raise ValidationError("El tipo de valor no es válido.")
        return tipo_valor

    def clean_tipo_negocio(self):
        """Validar que el tipo de negocio sea válido."""
        tipo_negocio = self.cleaned_data.get('tipo_negocio')
        tipos_validos = [choice[0] for choice in Publicacion.TIPO_NEGOCIO_CHOICES]
        if tipo_negocio not in tipos_validos:
            raise ValidationError("El tipo de negocio no es válido.")
        return tipo_negocio

    def clean_fecha_expiracion(self):
        """Validar que la fecha de expiración no sea anterior a hoy."""
        fecha_expiracion = self.cleaned_data.get('fecha_expiracion')
        if fecha_expiracion and fecha_expiracion < timezone.now().date():
            raise ValidationError("La fecha de expiración no puede ser una fecha pasada.")
        return fecha_expiracion

    def clean_comision_estimada(self):
        """Validar que la comisión estimada no sea negativa."""
        comision = self.cleaned_data.get('comision_estimada')
        if comision is not None and comision < 0:
            raise ValidationError("La comisión estimada no puede ser negativa.")
        return comision

    def save(self, commit=True):
        """Modificar el comportamiento del guardado para asignar título desde la propiedad."""
        instance = super().save(commit=False)
        instance.titulo = instance.id_propiedad.titulo
        if commit:
            instance.save()
        return instance


#=================================================================================================================
from django import forms
from .models import OperacionVenta
from propiedad.models import Propiedad

class OperacionVentaForm(forms.ModelForm):
    class Meta:
        model = OperacionVenta
        fields = [
            'descripcion',
            'valor_operacion'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'valor_operacion': forms.NumberInput(attrs={'class': 'form-control'}),
        }