from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class propietario(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=255)
    razon = models.CharField(max_length=255)
    representante = models.CharField(max_length=255)
    correo = models.EmailField(max_length=255)
    numero_contacto = models.CharField(max_length=9, null=True, blank=True)
    fecha_creacion = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'propietario'

    def clean(self):
        # Validar que el RUT no se repita
        if propietario.objects.filter(rut=self.rut).exclude(pk=self.pk).exists():
            raise ValidationError({'rut': 'El RUT ya está registrado.'})
        
        # Validar que el correo no se repita
        if propietario.objects.filter(correo=self.correo).exclude(pk=self.pk).exists():
            raise ValidationError({'correo': 'El correo ya está registrado.'})
        
    def __str__(self):
        return f"{self.razon} {self.representante} {self.rut}"
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(propietario, self).save(*args, **kwargs)
        
    