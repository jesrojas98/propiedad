from django.db import models
from django.utils import timezone
from login.models import corredor
from django.core.validators import RegexValidator
from operaciones.models import Publicacion

class contacto_propietario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    corredor = models.ForeignKey(corredor, on_delete=models.CASCADE, related_name='corredores')
    numero_contacto = models.CharField(max_length=9, null=True, blank=True,
        validators=[
            RegexValidator(
                regex=r'^[2-9]\d{8}$',
                message="El número de contacto debe tener 9 dígitos y comenzar con un número entre 2 y 9.",
                code='invalid_phone_number'
            )
        ]
    )
    mensaje = models.TextField()
    fecha = models.DateField(default=timezone.now) 
    class Meta:
        db_table = 'contacto_propietario'

    def __str__(self):
        return self.nombre
    
class contacto_interesado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    corredor = models.ForeignKey(corredor, on_delete=models.CASCADE, related_name='corredores_2')
    numero_contacto = models.CharField(max_length=9, null=True, blank=True,
        validators=[
            RegexValidator(
                regex=r'^[2-9]\d{8}$',
                message="El número de contacto debe tener 9 dígitos y comenzar con un número entre 2 y 9.",
                code='invalid_phone_number'
            )
        ]
    )
    id_publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE,related_name='publicaciones')
    mensaje = models.TextField()
    fecha = models.DateField(default=timezone.now) 

    class Meta:
        db_table = 'contacto_interesado'

    def __str__(self):
        return self.nombre
