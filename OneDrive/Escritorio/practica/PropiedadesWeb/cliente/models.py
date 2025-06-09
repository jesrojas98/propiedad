from django.db import models
from django.forms import ValidationError
from django.utils import timezone

# Create your models here.

class clientes(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    correo = models.EmailField(max_length=255)
    numero_contacto = models.CharField(max_length=255, null=True, blank=True)
    rut = models.CharField(max_length=255)
    #colocar valor default para la FK 
    id_corredor = models.CharField(max_length=255, default='1')

    class Meta:
        db_table = 'clientes'    

    def save(self, *args, **kwargs):
        self.full_clean()
        super(clientes, self).save(*args, **kwargs)      

    def clean(self):            
        # Validar que el correo no se repita
        if clientes.objects.filter(correo=self.correo).exclude(pk=self.pk).exists():
            raise ValidationError({'correo': 'El correo ya está registrado.'}); 

        # Validar que el RUT no se repita
        if clientes.objects.filter(rut=self.rut).exclude(pk=self.pk).exists():
            raise ValidationError({'rut': 'El RUT ya está registrado.'})
         
    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.rut} {self.correo} {self.numero_contacto}"
    