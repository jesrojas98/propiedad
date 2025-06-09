from django.db import models
from propiedad.models import Propiedad
from documentos.models import Documento
from login.models import corredor
from django.utils import timezone

class Comision(models.Model):
    ESTADO_VALE_VISTA_CHOICES = [
        ('Retenido', 'Retenido'),
        ('Aprobado', 'Aprobado'),
    ]

    id = models.AutoField(primary_key=True)
    id_propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    id_documento = models.ForeignKey(Documento, on_delete=models.CASCADE)  
    id_corredor = models.ForeignKey(corredor, on_delete=models.CASCADE)
    estado_vale_vista = models.CharField(max_length=255, choices=ESTADO_VALE_VISTA_CHOICES, default='Retenido')
    valor_vale_vista = models.IntegerField()
    fecha_creacion = models.DateField(default=timezone.now, null=True, blank=True)

    class Meta:
        db_table = 'comisiones_venta'


class Egresos(models.Model):

    id = models.AutoField(primary_key=True)
    id_corredor = models.ForeignKey(corredor, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    valor_egreso = models.IntegerField()
    fecha_creacion = models.DateField(default=timezone.now, null=True, blank=True)


    class Meta:
        db_table = 'egreso_dinero'