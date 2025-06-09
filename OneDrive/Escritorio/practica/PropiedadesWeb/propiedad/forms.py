from django import forms
from django.core.validators import RegexValidator
from .models import Propiedad, ImagenPropiedad, OpcionOtros

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = MultiFileInput
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        return data

class PropiedadForm(forms.ModelForm):
    TIPO_CREACION_CHOICES = [
        ('Venta', 'Venta'),
        ('Arriendo', 'Arriendo'),
    ]
    YES_OR_NOT_CHOICES = [
        ('Sí', 'Sí'),
        ('No', 'No'),
    ]
    nueva = forms.ChoiceField(
        choices=YES_OR_NOT_CHOICES,
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False
    )
    factibilidad_agua = forms.ChoiceField(choices=YES_OR_NOT_CHOICES, widget=forms.Select, required=False) 
    factibilidad_electricidad = forms.ChoiceField(choices=YES_OR_NOT_CHOICES, widget=forms.Select, required=False)
    factibilidad_alcantarillado = forms.ChoiceField(choices=YES_OR_NOT_CHOICES, widget=forms.Select, required=False)
    factibilidad_gas = forms.ChoiceField(choices=YES_OR_NOT_CHOICES, widget=forms.Select, required=False)
    posee_casa = forms.ChoiceField(choices=YES_OR_NOT_CHOICES, required=False)
    tipo_creacion = forms.ChoiceField(choices=TIPO_CREACION_CHOICES, widget=forms.Select, required=False)
    imagenes = MultiFileField(required=False)
    otros = forms.ModelMultipleChoiceField(queryset=OpcionOtros.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    # Validación de Número de Rol (Formato Chileno: "573-24")
    numero_rol = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{1,5}-\d{1,5}$',
                message='El Número de Rol debe tener el formato correcto (Ej: 573-24)',
                code='invalid_numero_rol'
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 573-24', 'class': 'form-control'})
    )
    

    class Meta:
        model = Propiedad
        fields = '__all__'
        widgets = {
            "id_propietario": forms.Select(attrs={"class": "custom-select"}),
            "numero_casa": forms.TextInput(attrs={"placeholder": "Ej: 56", "class": "form-control"}),
            "comuna": forms.TextInput(attrs={"placeholder": "Ej: La Florida", "class": "form-control"}),
            "calle": forms.TextInput(attrs={"placeholder": "Ej: Av. Principal", "class": "form-control"}),
            "region": forms.TextInput(attrs={"placeholder": "Ej: Metropolitana", "class": "form-control"}),
            "numero_calle": forms.NumberInput(attrs={"placeholder": "Ej: 1234", "class": "form-control"}),
            "titulo": forms.TextInput(attrs={"placeholder": "Ej: Casa con piscina", "class": "form-control"}),
            "descripcion": forms.Textarea(
                attrs={"placeholder": "Ej: Casa de 3 pisos con terraza y jardín...", "class": "form-control", "rows": 3}
            ),
            "numero_lote": forms.TextInput(attrs={"placeholder": "Ej: 5B", "class": "form-control"}),
            "video": forms.FileInput(attrs={"class": "form-control-file"}),
            "superficie_terreno": forms.NumberInput(attrs={"placeholder": "Ej: 500", "class": "form-control"}),
            "superficie_construida": forms.NumberInput(attrs={"placeholder": "Ej: 120", "class": "form-control"}),
            "anio_construccion": forms.NumberInput(attrs={"placeholder": "Ej: 1998", "class": "form-control"}),
            "gastos_comunes": forms.NumberInput(attrs={"placeholder": "Ej: 150000", "class": "form-control"}),
            "dormitorios": forms.NumberInput(attrs={"placeholder": "Ej: 3", "class": "form-control"}),
            "banios": forms.NumberInput(attrs={"placeholder": "Ej: 2", "class": "form-control"}),
            "estacionamiento": forms.NumberInput(attrs={"placeholder": "Ej: 1", "class": "form-control"}),
            "bodegas": forms.NumberInput(attrs={"placeholder": "Ej: 1", "class": "form-control"}),
            "pisos": forms.NumberInput(attrs={"placeholder": "Ej: 2", "class": "form-control"}),
            "oficinas": forms.TextInput(attrs={"placeholder": "Ej: Oficina 1, Oficina 2", "class": "form-control"}),
            "recintos": forms.TextInput(attrs={"placeholder": "Ej: Sala de estar, Comedor", "class": "form-control"}),
            "sector": forms.TextInput(attrs={"placeholder": "Ej: Residencial", "class": "form-control"}),
            "factibilidad_agua": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "factibilidad_electricidad": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "factibilidad_alcantarillado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "factibilidad_gas": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "fecha_creacion": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "codigo_propiedad": forms.TextInput(attrs={"placeholder": "Ej: A-12345", "class": "form-control"}),
        }

    def clean_imagenes(self):
        imagenes = self.cleaned_data.get('imagenes')
        if imagenes and len(imagenes) > 15:
            raise forms.ValidationError("Solo se permiten un máximo de 15 imágenes.")
        return imagenes
    
    def clean_codigo_propiedad(self):
        codigo = self.cleaned_data.get('codigo_propiedad')
        
        # Si no hay código, no hay problema
        if not codigo:
            return codigo
            
        # Obtener la instancia actual (si existe)
        instance = getattr(self, 'instance', None)
        
        # Verificar si ya existe una propiedad con el mismo código, excluyendo la instancia actual
        if instance and instance.pk:
            # Excluir la propiedad actual de la validación
            if Propiedad.objects.filter(codigo_propiedad=codigo).exclude(pk=instance.pk).exists():
                raise forms.ValidationError("Ya existe una propiedad con este código. Por favor, use otro.")
        else:
            # Para nuevas propiedades, verificar si el código ya existe
            if Propiedad.objects.filter(codigo_propiedad=codigo).exists():
                raise forms.ValidationError("Ya existe una propiedad con este código. Por favor, use otro.")
                
        return codigo
