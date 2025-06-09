from django import forms
from .models import contacto_interesado
from .models import contacto_propietario
from login.models import corredor

class contactoForm(forms.ModelForm):
    class Meta:
        model = contacto_propietario
        fields = ['nombre', 'apellido', 'correo', 'numero_contacto', 'corredor', 'mensaje']

    def __init__(self, *args, **kwargs):
        super(contactoForm, self).__init__(*args, **kwargs)
        self.fields['corredor'].queryset = corredor.objects.all()
        self.fields['corredor'].label_from_instance = lambda obj: f"Nombre: {obj.nombre} Correo: {obj.correo}"
    
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        apellido = cleaned_data.get("apellido")
        correo = cleaned_data.get("correo")
        numero_contacto = cleaned_data.get("numero_contacto")
        mensaje = cleaned_data.get("mensaje")


        if nombre:
            cleaned_data["nombre"] = nombre.strip()
        if apellido:
            cleaned_data["apellido"] = apellido.strip()
        if correo:
            cleaned_data["correo"] = correo.strip()
        if numero_contacto:
            numero_contacto = numero_contacto.replace(" ", "").strip()  # Elimina espacios internos
            if not numero_contacto.isdigit():
                raise forms.ValidationError("El número de contacto solo debe contener dígitos.")
            if len(numero_contacto) != 9:
                raise forms.ValidationError("El número de contacto debe tener exactamente 9 dígitos.")
            if not numero_contacto.startswith(('2', '3', '4', '5', '6', '7', '8', '9')):  # Comenzar con 9 para móviles chilenos
                raise forms.ValidationError("El número de contacto debe comenzar con un dígito entre 2 y 9.")
            cleaned_data["numero_contacto"] = numero_contacto  # Guardar el valor limpio
        
        if mensaje:
            cleaned_data["mensaje"] = mensaje.strip()

        return cleaned_data  

class ContactoInteresadoForm(forms.ModelForm):
    class Meta:
        model = contacto_interesado
        fields = ['nombre', 'apellido', 'correo', 'numero_contacto', 'mensaje']

