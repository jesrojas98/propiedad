from django.utils import timezone
from django import forms
from django.db import models
from propiedad.models import Propiedad


class Documento(models.Model):
    id = models.AutoField(primary_key=True)
    id_propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)  # Relación con la propiedad
    tipo_documento = models.CharField(max_length=255, null=False)
    pdf_documento = models.FileField(upload_to='documentos/docu_venta/', null=True, blank=True)  # Campo FileField correcto
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    fecha = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"Documento para {self.tipo_docu} de {self.id_propiedad}"

