from django import forms
from django.core.validators import RegexValidator
from .models import corredor
from itertools import cycle

class CorredorLoginForm(forms.Form):
    correo = forms.EmailField()
    contrasenia = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo')
        contrasenia = cleaned_data.get('contrasenia')
        if correo:
            cleaned_data["correo"] = correo.strip()
        if contrasenia:
            cleaned_data["contrasenia"] = contrasenia.strip()
        return cleaned_data
    
class RegistroUsuarioForm(forms.ModelForm):
    contrasenia = forms.CharField(widget=forms.PasswordInput())
    confirmar_contrasenia = forms.CharField(widget=forms.PasswordInput())

    rut = forms.CharField(
        validators=[RegexValidator(
            regex=r'^[0-9]+-[0-9Kk]$',
            message='El RUT debe tener el formato correcto (Ej: 12345678-9 o 1234567-K).',
            code='invalid_rut'
        )],widget=forms.TextInput(attrs={'placeholder': '12345678-9'})
    )

    class Meta:
        model = corredor
        fields = ['nombre', 'apellido', 'rut', 'correo', 'numero_contacto', 'contrasenia']

    def clean_rut(self):
        """ Limpia y valida el RUT ingresado """
        rut = self.cleaned_data.get("rut")

        if rut:
            # Eliminar puntos y convertir en mayúsculas
            rut = rut.replace(".", "").replace("-", "").upper()

            # Verificar que tenga el largo adecuado (7-8 dígitos + DV)
            if not 8 <= len(rut) <= 9:
                raise forms.ValidationError("El RUT ingresado no tiene un formato válido.")

            # Separar número y dígito verificador
            rut_sin_dv, dv = rut[:-1], rut[-1]

            # Validar el dígito verificador
            if calcular_dv(rut_sin_dv) != dv:
                raise forms.ValidationError("El dígito verificador del RUT es incorrecto.")

            # Validar que no esté registrado en la base de datos
            if corredor.objects.filter(rut=rut).exists():
                raise forms.ValidationError("El RUT ya está registrado.")

        return rut

    def clean(self):
        cleaned_data = super().clean()
        contrasenia = cleaned_data.get('contrasenia')
        confirmar_contrasenia = cleaned_data.get('confirmar_contrasenia')
        correo = cleaned_data.get('correo')

        # Validar que las contraseñas coincidan
        if contrasenia and confirmar_contrasenia and contrasenia != confirmar_contrasenia:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        # Validar que el correo no esté repetido
        if correo and corredor.objects.filter(correo=correo).exists():
            raise forms.ValidationError("El correo ya está registrado.")

        return cleaned_data

def calcular_dv(rut):
    """ Calcula el dígito verificador de un RUT chileno """
    reversed_digits = map(int, reversed(rut))
    factors = cycle(range(2, 8))
    suma = sum(d * f for d, f in zip(reversed_digits, factors))
    mod = (-suma) % 11
    return 'K' if mod == 10 else str(mod)

class CambiarContraseniaForm(forms.Form):
    nueva_contrasenia = forms.CharField(
        widget=forms.PasswordInput,
        label="Nueva Contraseña"
    )
    confirmar_contrasenia = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmar Contraseña"
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva_contrasenia = cleaned_data.get("nueva_contrasenia")
        confirmar_contrasenia = cleaned_data.get("confirmar_contrasenia")

        if nueva_contrasenia and confirmar_contrasenia:
            if nueva_contrasenia != confirmar_contrasenia:
                raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data
