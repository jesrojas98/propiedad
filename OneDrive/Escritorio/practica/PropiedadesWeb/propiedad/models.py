from django.db import models
from propietarios.models import propietario
from django.utils import timezone
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from login.models import corredor


class OpcionOtros(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Propiedad(models.Model):
    id = models.AutoField(primary_key=True)
    id_propietario = models.ForeignKey(propietario, on_delete=models.CASCADE)
    id_corredor_encargado = models.ForeignKey(corredor, on_delete=models.SET_NULL, null=True, blank=True)
    numero_casa = models.CharField(max_length=255, null=True, blank=True) #
    comuna = models.CharField(max_length=255) #
    calle = models.CharField(max_length=255) #
    region = models.CharField(max_length=255) #
    numero_calle = models.IntegerField(null=True, blank=True) #
    numero_rol = models.CharField(max_length=255) #
    titulo = models.CharField(max_length=100) #
    nueva = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255) #
    posee_casa = models.BooleanField(null=True, blank=True) 
    numero_lote = models.CharField(max_length=45, null=True, blank=True) #
    video = models.FileField(upload_to='video/', null=True, blank=True)
    superficie_terreno = models.CharField(max_length=255, null=True, blank=True)
    superficie_construida = models.CharField(max_length=255, null=True, blank=True)
    anio_construccion = models.CharField(max_length=255, null=True, blank=True)
    gastos_comunes = models.CharField(max_length=255, null=True, blank=True)
    dormitorios = models.CharField(max_length=255, null=True, blank=True)
    banios = models.CharField(max_length=255, null=True, blank=True)
    estacionamiento = models.CharField(max_length=255, null=True, blank=True)
    bodegas = models.CharField(max_length=255, null=True, blank=True)
    pisos = models.CharField(max_length=255, null=True, blank=True)
    otros = models.ManyToManyField(OpcionOtros, blank=True)
    oficinas = models.CharField(max_length=255, null=True, blank=True)
    recintos = models.CharField(max_length=255, null=True, blank=True)
    sector = models.CharField(max_length=255, null=True, blank=True)
    factibilidad_agua = models.CharField(max_length=50)
    factibilidad_electricidad = models.CharField(max_length=50)
    factibilidad_alcantarillado = models.CharField(max_length=50)
    factibilidad_gas = models.CharField(max_length=50)
    fecha_creacion = models.DateField(default=timezone.now, null=True, blank=True)
    tipo_propiedad = models.CharField(max_length=255, null=True, blank=True)
    codigo_propiedad = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        db_table = 'propiedad'

    def __str__(self):
        return f"{self.titulo} - {self.calle} {self.numero_calle}"

    def delete(self, *args, **kwargs):
        for imagen in self.imagenes.all():
            imagen.imagen.delete()
            imagen.delete()
        super().delete(*args, **kwargs)

class ImagenPropiedad(models.Model):
    propiedad = models.ForeignKey(Propiedad, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagen/', null=True, blank=True)

    class Meta:
        db_table = 'imagen_propiedad'



        