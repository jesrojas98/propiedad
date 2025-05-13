from django.db import models
from django.utils import timezone
from propiedad.models import Propiedad
from documentos.models import Documento
from django.core.exceptions import ValidationError
from login.models import corredor
import json
import requests
from datetime import datetime



class Publicacion(models.Model):
    TIPO_PUBLICACION_CHOICES = [
        ('Venta', 'Venta'),
        ('Arriendo', 'Arriendo'),
    ]
    
    TIPO_VALOR_CHOICES = [
        ('CLP', 'CLP'),
        ('UF', 'UF'),
    ]
    
    TIPO_NEGOCIO_CHOICES = [
        ('Particular', 'Particular'),
        ('Inmobiliaria', 'Inmobiliaria'),
    ]

    id = models.AutoField(primary_key=True)
    id_propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    id_corredor_encargado = models.ForeignKey(corredor, on_delete=models.SET_NULL, null=True, blank=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    valor = models.IntegerField()
    tipo_publicacion = models.CharField(max_length=50, choices=TIPO_PUBLICACION_CHOICES)
    tipo_valor = models.CharField(max_length=50, choices=TIPO_VALOR_CHOICES)
    tipo_negocio = models.CharField(max_length=50, choices=TIPO_NEGOCIO_CHOICES)
    destacada = models.BooleanField(default=False)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateField()
    comision_estimada = models.IntegerField()


    class Meta:
        db_table = 'publicacion'

    def clean(self):
        if self.fecha_expiracion and self.fecha_expiracion < timezone.now().date():
            raise ValidationError("La fecha de expiración no puede ser anterior a hoy.")

    def save(self, *args, **kwargs):
        if not self.comision_estimada:
            self.comision_estimada = int(self.valor * 0.04)  # Calculando 4% de comisión
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
    

from login.models import corredor  # Importar el modelo corredor

class OperacionVenta(models.Model):
    # Estados de la operación (los mantienes igual)
    ESTADO_AGENDAMIENTO_CHOICES = [('NO INICIADA', 'NO INICIADA'), ('AGENDADA', 'AGENDADA'), ('ANULADA', 'ANULADA'), ('REALIZADA', 'REALIZADA')]
    ESTADO_ANTECEDENTES_CHOICES = [('NO INICIADA', 'NO INICIADA'), ('OMITIDA', 'OMITIDA'), ('ANULADA', 'ANULADA'), ('REALIZADA', 'REALIZADA')]
    ESTADO_NEGOCIO_CHOICES = [('NO INICIADA', 'NO INICIADA'), ('PRESENTADA', 'PRESENTADA'), ('RECHAZADA', 'RECHAZADA'), ('ANULADA', 'ANULADA'), ('ACEPTADA', 'ACEPTADA')]
    ESTADO_PROMESA_CHOICES = [('NO INICIADA', 'NO INICIADA'), ('PRESENTADA', 'PRESENTADA'), ('RECHAZADA', 'RECHAZADA'), ('ANULADA', 'ANULADA'), ('ACEPTADA', 'ACEPTADA')]
    ESTADO_ESCRITURA_CHOICES = [('NO INICIADA', 'NO INICIADA'), ('PRESENTADA', 'PRESENTADA'), ('RECHAZADA', 'RECHAZADA'), ('ANULADA', 'ANULADA'), ('ACEPTADA', 'ACEPTADA')]
    ESTADO_INSCRIPCION_CHOICES = [('NO INICIADA', 'NO INICIADA'), ('PRESENTADA', 'PRESENTADA'), ('RECHAZADA', 'RECHAZADA'), ('ANULADA', 'ANULADA'), ('ACEPTADA', 'ACEPTADA')]
    ESTADO_ENTREGA_CHOICES = [('NO INICIADA', 'NO INICIADA'), ('CANCELADA', 'CANCELADA'), ('ANULADA', 'ANULADA'), ('ENTREGADA', 'ENTREGADA')]

    # Claves primarias y foráneas
    id = models.AutoField(primary_key=True)
    id_propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)  
    id_documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    id_corredor = models.ForeignKey(corredor, on_delete=models.SET_NULL, null=True, blank=True)  # NUEVO
    progreso = models.IntegerField(default=0)  # Progreso automático en porcentaje (0-100)

    # Información de la operación
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    estado_antecedentes = models.CharField(max_length=255, choices=ESTADO_ANTECEDENTES_CHOICES, null=True, blank=True, default='NO DATA')
    estado_agendamiento = models.CharField(max_length=255, choices=ESTADO_AGENDAMIENTO_CHOICES, null=True, blank=True, default='NO DATA')
    estado_cierre_negocio = models.CharField(max_length=255, choices=ESTADO_NEGOCIO_CHOICES, null=True, blank=True, default='NO DATA')
    estado_promesa = models.CharField(max_length=255, choices=ESTADO_PROMESA_CHOICES, null=True, blank=True, default='NO DATA')
    estado_escritura = models.CharField(max_length=255, choices=ESTADO_ESCRITURA_CHOICES, null=True, blank=True, default='NO DATA')
    estado_inscripcion = models.CharField(max_length=255, choices=ESTADO_INSCRIPCION_CHOICES, null=True, blank=True, default='NO DATA')
    estado_entrega = models.CharField(max_length=255, choices=ESTADO_ENTREGA_CHOICES, null=True, blank=True, default='NO DATA')

    # Datos financieros y temporales
    fecha_creacion_operacion = models.DateTimeField(auto_now_add=True)
    comision_operacion = models.IntegerField()
    valor_operacion = models.IntegerField()
    
    class Meta:
        db_table = 'Operacion_Venta'
    
    def __str__(self):
        return f"Operación {self.id} - {self.id_propiedad.titulo}"

class Mindicador:
    def __init__(self, indicador):
        self.indicador = indicador

    def obtener_ultimo_mes(self):
        # Realizamos la solicitud a la API para obtener los datos del indicador
        url = f'https://mindicador.cl/api/{self.indicador}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()

            # Extraemos la serie de datos
            serie = data.get("serie", [])
            
            if serie:
                # Filtramos los datos para obtener el último mes
                # Primero, ordenamos la serie por fecha (de más reciente a más antiguo)
                serie.sort(key=lambda x: x['fecha'], reverse=True)

                # Extraemos el valor y la fecha del último mes
                ultimo_dato = serie[0]
                fecha_ultimo_mes = datetime.strptime(ultimo_dato["fecha"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
                valor_ultimo_mes = ultimo_dato["valor"]

                return {"fecha": fecha_ultimo_mes, "valor": valor_ultimo_mes}

        return None  # Si no se obtienen datos válidos