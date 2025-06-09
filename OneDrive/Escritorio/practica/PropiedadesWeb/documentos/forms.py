from django import forms
from .models import Documento

class DocumentosForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['tipo_documento', 'pdf_documento', 'descripcion']  # Eliminamos id_propiedad

    pdf_documento = forms.FileField(label="Documento PDF", required=True)
    descripcion = forms.CharField(
        max_length=255,
        label="Descripción",
        required=True,  # Puedes cambiarlo a False si quieres que sea opcional
        widget=forms.Textarea(attrs={'rows': 3})
    )
