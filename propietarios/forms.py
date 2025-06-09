from django import forms
from django.core.validators import RegexValidator
from .models import propietario
from itertools import cycle

class RegistroPropietario(forms.ModelForm):
    rut = forms.CharField(
        validators=[RegexValidator(
            regex=r'^[0-9]+-[0-9Kk]$',
            message='El RUT debe tener el formato correcto (Ej: 12345678-9 o 1234567-K).',
            code='invalid_rut'
        )],widget=forms.TextInput(attrs={'placeholder': '12345678-9'})
    )

    class Meta:
        model = propietario
        fields = ['rut', 'razon', 'representante', 'correo', 'numero_contacto']
        widgets = {
            'razon': forms.TextInput(attrs={'placeholder': 'Nombre de la empresa'}),
            'representante': forms.TextInput(attrs={'placeholder': 'Juan Pérez'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'numero_contacto': forms.TextInput(attrs={'placeholder': '912345678'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get("correo")
        rut = cleaned_data.get("rut")
        razon = cleaned_data.get("razon")
        representante = cleaned_data.get("representante")
        numero_contacto = cleaned_data.get("numero_contacto")

        # Eliminar espacios en blanco de los extremos
        if razon:
            cleaned_data["razon"] = razon.strip()
        if representante:
            cleaned_data["representante"] = representante.strip()
        if correo:
            cleaned_data["correo"] = correo.strip()
        if rut:
            cleaned_data["rut"] = rut.strip()
        if numero_contacto:
            cleaned_data["numero_contacto"] = numero_contacto.strip()

        # Validar que el RUT no se repita
        if rut and propietario.objects.filter(rut=rut).exists():
            raise forms.ValidationError("El RUT ya está registrado.")
        
        # Validar que el correo no se repita
        if correo and propietario.objects.filter(correo=correo).exists():
            raise forms.ValidationError("El correo ya está registrado.")
        
        # Validar el dígito verificador del RUT
        if rut:
            try:
                rut_sin_dv, dv = rut[:-2], rut[-1].upper()
                if calcular_dv(rut_sin_dv) != dv:
                    raise forms.ValidationError("El dígito verificador del RUT es incorrecto.")
            except IndexError:
                raise forms.ValidationError("El formato del RUT es incorrecto.")
        
        return cleaned_data

def calcular_dv(rut):
    """ Calcula el dígito verificador de un RUT chileno """
    reversed_digits = map(int, reversed(rut))
    factors = cycle(range(2, 8))
    suma = sum(d * f for d, f in zip(reversed_digits, factors))
    mod = (-suma) % 11
    return 'K' if mod == 10 else str(mod)
# ----------------------------------------------------------------------------------------------------------------------------

class EditarPropietario(forms.ModelForm):
    class Meta:
        model = propietario
        fields = ['razon', 'representante', 'correo', 'numero_contacto']
        widgets = {
            'razon': forms.TextInput(attrs={'placeholder': 'Nombre de la empresa'}),
            'representante': forms.TextInput(attrs={'placeholder': 'Juan Pérez'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'numero_contacto': forms.TextInput(attrs={'placeholder': '912345678'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("razon")
        apellido = cleaned_data.get("representante")
        correo = cleaned_data.get("correo")
        numero_contacto = cleaned_data.get("numero_contacto")
        
        # Eliminar espacios en blanco de los extremos
        if nombre:
            cleaned_data["razon"] = nombre.strip()
        if apellido:
            cleaned_data["representante"] = apellido.strip()
        if correo:
            cleaned_data["correo"] = correo.strip()
        if numero_contacto:
            cleaned_data["numero_contacto"] = numero_contacto.strip()

        # Validar que el correo no se repita
        if correo and propietario.objects.filter(correo=correo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError({"correo": "El correo ya está registrado."})
        
        # Validar que el número no sea menor a 9 dígitos y que sea solo números
        if numero_contacto:
            if len(numero_contacto) != 9:
                raise forms.ValidationError({"numero_contacto": "El número de contacto debe tener 9 dígitos."})
            if not numero_contacto.isdigit():
                raise forms.ValidationError({"numero_contacto": "El número de contacto debe contener sólo dígitos."})
        
        return cleaned_data
