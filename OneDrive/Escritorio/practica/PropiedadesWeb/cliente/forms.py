from django import forms
from django.core.validators import RegexValidator
from .models import clientes 
from itertools import cycle

class ClienteForm(forms.ModelForm):
    class Meta:
        model = clientes
        fields = ['nombre', 'apellido', 'correo', 'numero_contacto', 'rut']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Juan'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Pérez'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'numero_contacto': forms.TextInput(attrs={'placeholder': '912345678'}),
            'rut': forms.TextInput(attrs={'placeholder': '12345678-9'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get("correo")
        nombre = cleaned_data.get("nombre")
        apellido = cleaned_data.get("apellido")
        numero_contacto = cleaned_data.get("numero_contacto")
        rut = cleaned_data.get("rut")

        # Eliminar espacios en blanco de los extremos
        if nombre:
            cleaned_data["nombre"] = nombre.strip()
        if apellido:
            cleaned_data["apellido"] = apellido.strip()
        if correo:
            cleaned_data["correo"] = correo.strip()
        if numero_contacto:
            cleaned_data["numero_contacto"] = numero_contacto.strip()
        if rut:
            cleaned_data["rut"] = rut.strip()

        # Validar que el correo no se repita
        if correo and clientes.objects.filter(correo=correo).exists():
            raise forms.ValidationError("El correo ya está registrado.")
        
        # Validar que el RUT no se repita
        if rut and clientes.objects.filter(rut=rut).exists():
            raise forms.ValidationError("El RUT ya está registrado.")
        
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
    rut = rut.replace(".", "").replace("-", "")
    reversed_digits = map(int, reversed(rut))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    mod = (-s) % 11
    return 'K' if mod == 10 else str(mod)

# ----------------------------------------------------------------------------------------------------------------------------

class EditarCliente(forms.ModelForm):
    class Meta:
        model = clientes
        fields = ['nombre', 'apellido', 'correo', 'numero_contacto']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Juan'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Pérez'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'numero_contacto': forms.TextInput(attrs={'placeholder': '912345678'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get("correo")
        nombre = cleaned_data.get("nombre")
        apellido = cleaned_data.get("apellido")
        numero_contacto = cleaned_data.get("numero_contacto")

        # Eliminar espacios en blanco de los extremos
        if nombre:
            cleaned_data["nombre"] = nombre.strip()
        if apellido:
            cleaned_data["apellido"] = apellido.strip()
        if correo:
            cleaned_data["correo"] = correo.strip()
        if numero_contacto:
            cleaned_data["numero_contacto"] = numero_contacto.strip()

        # Validar que el correo no se repita
        if correo and clientes.objects.filter(correo=correo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError({"correo": "El correo ya está registrado."})
        
        # Validar que el número de contacto tenga 9 dígitos y solo contenga números
        if numero_contacto:
            if len(numero_contacto) != 9:
                raise forms.ValidationError({"numero_contacto": "El número de contacto debe tener 9 dígitos."})
            if not numero_contacto.isdigit():
                raise forms.ValidationError({"numero_contacto": "El número de contacto debe contener sólo dígitos."})
        
        return cleaned_data
